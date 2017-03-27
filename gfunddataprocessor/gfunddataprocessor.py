# coding: utf-8

from __future__ import division

import datetime as dtime
import os
import re
import gzip
import time
import multiprocessing as mp

import numpy as np
import pandas as pd
import tick_pb2 as tp

from globallogger import logger
from cStringIO import StringIO
from futureTradeTime import TRADETIME
from futureTradeTime import FUTURES
from mongo import MongoDB

################################################################
#   mongodb are choosed as the defualt database
#   maybe we should write a wrapper to seperate
#   the database query operation
#   this module maybe helpful later:
#   sqltomongo: https://github.com/klausdk/sqltomongodb
#   but that's a tedious work, do it later
################################################################
# mdb = MongoDB()
# db = mdb.client['futures']
# coll_zhongxin = db['future2']
# coll_yinhe = db['future_yinhe4']

################################################################
# the return of all "get_..." function has a common format:
# DataFrame of Pandas
################################################################

ZHONGXIN = 0
YINHE = 1
SZ = 'SZ'
SH = 'SH'

STOCK_TICK_PATH = '/data/tdb/tick.pb.gz'
MARKET = {'1011': 'sh', '1012': 'sz'}

DAY_TYPE = 0
NIGHT_TYPE = 1

COLUMNS = [e.name for e in tp.Tick.DESCRIPTOR.fields]
COLUMNS.append('instrument_id')
COLUMNS.append('type')
PRICE_LIST = [
    'price', 'turnover', 'acc_turnover', 'high', 'low', 'open', 'pre_close',
    'pre_close', 'settle', 'pre_settle', 'cur_delta',
    'ask_price1', 'ask_price2', 'ask_price3', 'ask_price4', 'ask_price5',
    'ask_price6', 'ask_price7', 'ask_price8', 'ask_price9', 'ask_price10',
    'bid_price1', 'bid_price2', 'bid_price3', 'bid_price4', 'bid_price5',
    'bid_price6', 'bid_price7', 'bid_price8', 'bid_price9', 'bid_price10',
    'ask_avg_price', 'bid_avg_price', 'index']
PRICE_ORDER = [COLUMNS.index(e) for e in PRICE_LIST]
ALL = COLUMNS
COLUMNS_SET = set(COLUMNS)
DEFAULT = ['instrument_id', 'price', 'bid_price1', 'bid_volume1',
           'ask_price1', 'ask_volume1', 'interest', 'volume']

process_num = 8


def set_process_num(n):
    global process_num
    process_num = n


def _is_futures(symbol):
    symbol = symbol.upper()
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    ID_parts = pat_future.search(symbol)

    if ID_parts:
        return True
    else:
        pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
        ID_parts = pat_stock.search(symbol)
        assert ID_parts is not None
        return False


def _get_current_coll(data_source):
    mdb = MongoDB()
    db = mdb.client['futures']
    if data_source == ZHONGXIN:
        coll_now = db['future2']
    elif data_source == YINHE:
        coll_now = db['future_yinhe4']
    else:
        coll_now = None
    return coll_now


# start_time: typical -- 20150102-09:30:15.389
#             allowed -- 20150102
#             allowed -- 20150102-09[:30[:15[.389]]]
def get_tick_data(symbol, start, end, columns=DEFAULT,
                  data_source=ZHONGXIN, pad=False):
    symbol = symbol.upper()
    if type(start) != type(end):
        logger.error('different type found in datetime')
        return None

    # 兼容字符串和datetime，Timestamp
    if not hasattr(start, 'strftime'):
        pat = re.compile(r'^([a-zA-Z]+)(\d+){0,1}')
        try:
            futureID = pat.search(symbol).group(1)
        except:
            return None
        s_date, s_time = _extract_contract_time(start, futureID)
        e_date, e_time = _extract_contract_time(end, futureID)
        if s_date is None or e_date is None:
            logger.error('invalid time format found!')
            return None
        start_timestamp = pd.Timestamp(str(s_date)+' '+s_time)
        end_timestamp = pd.Timestamp(str(e_date)+' '+e_time)
    else:
        s_date = start.strftime('%Y%m%d')
        e_date = end.strftime('%Y%m%d')
        start_timestamp = start
        end_timestamp = end

    res = get_day_tick(symbol, (s_date, e_date), columns, merge=True,
                       data_source=data_source, pad=pad)
    if res is not None:
        res = res[start_timestamp: end_timestamp]
    return res


def get_main_contract(fuid, days, columns=DEFAULT, merge=True,
                      data_source=ZHONGXIN, pad=False):
    if type(days) == int or type(days) == str:
        days = [days]

    if type(days) != tuple and type(days) != list:
        logger.error('parameter error!!')
        return None

    if type(days) == tuple and len(days) != 2:
        logger.error('parameter error!!')
        return None

    mdb1 = MongoDB()
    db1 = mdb1.client['futures']
    coll1 = db1['main_contracts']
    coll_now = _get_current_coll(data_source)

    if type(days) == list:
        cursor = coll1.find(
            {
                'TradingDay': {'$in': [int(e) for e in days]},
                'InstrumentID': {'$regex': re.compile('^'+fuid+r'\d+$')}})
    else:
        cursor = coll1.find(
            {
                'TradingDay': {'$gte': int(days[0]), '$lte': int(days[1])},
                'InstrumentID': {'$regex': re.compile('^'+fuid+r'\d+$')}})
    df_main = pd.DataFrame(list(cursor))
    if df_main.empty:
        logger.warn('found nothing, maybe not trading days')
        return None
    pairs = zip(df_main.TradingDay, df_main.InstrumentID)

    if df_main.empty:
        return None

    # 一次取出冗余的数据后进行筛选， 减少query次数
    cursor = coll_now.find(
        {
            'TradingDay': {'$in': df_main.TradingDay.tolist()},
            'InstrumentID': {'$in': list(set(df_main.InstrumentID.tolist()))}})
    df_tmp = pd.DataFrame(list(cursor))
    df_res = df_tmp[[(
        df_tmp.loc[i]['TradingDay'], df_tmp.loc[i]['InstrumentID'])
        in pairs for i in range(len(df_tmp.index))]]

    if len(df_res) == 0:
        return None
    elif len(df_res) < 5:
        res = _decode_tick_data(df_res, columns, pad)
    else:
        pool = mp.Pool(processes=process_num)
        res = []
        for df in _chunks(df_res, 1):
            res.append(pool.apply_async(_decode_tick_data, (df, columns, pad)))
        pool.close()
        pool.join()

        res = map(lambda ret: ret.get(), res)
        # flatten the list.
        res = [item for sublist in res for item in sublist]

    if merge:
        res = pd.concat(res)

    return res

##############################################################
# 这里先只考虑期货， 股票数据录入了再重构， 一步一步来
##############################################################


def _get_stock_from_files(symbol, days, market_id=None):
    # 20121101 20121102
    alldays = os.listdir(STOCK_TICK_PATH)
    if type(days) == list:
        targets = [str(e) for e in days if str(e) in alldays]
    elif type(days) == tuple:
        targets = [e for e in alldays if e >= str(days[0])
                   and e <= str(days[1])]
    else:
        logger.error('invalid type of parameter days')
        return None
    reslist = []
    for day in targets:
        sdict = {}
        day_path = os.path.join(STOCK_TICK_PATH, day)
        # 1101, 1102
        if market_id not in [SZ, SH]:
            logger.error("invalid market "+str(market_id))
            return None
        elif market_id == SZ:
            market = '1012'
        elif market_id == SH:
            market = '1011'

        market_path = os.path.join(day_path, market)
        name = symbol+'.pb.gz'
        # 124081.pb.gz, 124895.pb.gz
        if name not in os.listdir(market_path):
            continue
        sdict['InstrumentID'] = symbol+'.'+MARKET[market]
        sdict['Type'] = 0
        sdict['content'] = open(os.path.join(market_path, name),
                                'rb').read()
        sdict['TradingDay'] = int(day)
        reslist.append(sdict)
    return pd.DataFrame(reslist)


def get_day_tick(symbol, days, columns=DEFAULT, merge=True,
                 data_source=ZHONGXIN, pad=False):
    # 判断是股票还是期货
    flag = 'FUTURE'
    symbol = symbol.upper()
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
    ID_parts = pat_future.search(symbol)
    security_ID = fdate = None
    if ID_parts:
        security_ID, fdate = ID_parts.groups()
    else:
        ID_parts = pat_stock.search(symbol)
        if ID_parts is None:
            logger.error('invalid symbol '+symbol)
            return None
        security_ID, market = ID_parts.groups()
        flag = 'STOCK'

    # 查询期货代码是否在数据库中
    if security_ID not in FUTURES and flag == 'FUTURE':
        logger.error(security_ID + ' not found in futures base')
        return None

    if type(days) == int or type(days) == str:
        days = [days]

    if type(days) != tuple and type(days) != list:
        logger.error('parameter type error!!')
        return None

    if type(days) == tuple and len(days) != 2:
        logger.error('parameter type error!!')
        return None

    if not all([isinstance(e, type(days[0])) for e in days]):
        logger.error('parameter type error!!')
        return None

    coll_now = _get_current_coll(data_source)

    if not fdate and flag == 'FUTURE':
        return get_main_contract(security_ID, days, columns,
                                 merge, data_source, pad)

    # 从mongodb中获取期货数据
    if flag == 'FUTURE':
        if hasattr(days[0], 'strftime'):
            days = [e.strftime('%Y%m%d') for e in days]
        if type(days) == list:
            cursor = coll_now.find({
                'TradingDay': {'$in': [int(i) for i in days]},
                'InstrumentID': symbol})

        if type(days) == tuple:
            cursor = coll_now.find({
                'TradingDay': {'$gte': int(days[0]), '$lte': int(days[1])},
                'InstrumentID': symbol})

        df_res = pd.DataFrame(list(cursor))
    # 从文件系统中获取股票数据
    else:
        df_res = _get_stock_from_files(security_ID, days, market)

    if len(df_res) == 0:
        return None
    elif len(df_res) < 5:
        res = _decode_tick_data(df_res, columns, pad)
    else:
        pool = mp.Pool(processes=process_num)
        res = []
        for df in _chunks(df_res, 1):
            res.append(pool.apply_async(_decode_tick_data, (df, columns, pad)))
        pool.close()
        pool.join()

        res = map(lambda ret: ret.get(), res)
        # flatten the list.
        res = [item for sublist in res for item in sublist]

    if merge:
        res = pd.concat(res)

    return res


def get_filled_tick_data(symbol, start, end=None):
    pass


def get_bar_data():
    pass


# TODO(reed): This method is unstable(since the structure of `TRADETIME` is not
# reasonable), it may need modification.
def _get_rest_time(symbol, day, time_type=None):
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
    ID_parts = pat_future.search(symbol)
    security_ID = fdate = None
    if ID_parts:
        security_ID, fdate = ID_parts.groups()
        flag = 'FUTURE'
    else:
        ID_parts = pat_stock.search(symbol)
        assert ID_parts is not None
        security_ID, market = ID_parts.groups()
        flag = 'STOCK'

    if flag == 'FUTURE':
        if time_type == DAY_TYPE:
            # FIXME(reed): Commodity futures rests at [10:15, 10:30].
            # start1 = TRADETIME[security_ID]['day']['open1']
            end1 = TRADETIME[security_ID]['day']['close1']
            start2 = TRADETIME[security_ID]['day']['open2']
            # end2 = TRADETIME[security_ID]['day']['close2']
            # 如果是股指期货， 中间日盘时间进行过调整， 需要判断
            if 'dayChange' in TRADETIME[security_ID]['day']:
                trading_day = day.year * 10000 + day.month * 100 + day.day
                day_change = int(TRADETIME[security_ID]['day']['dayChange'])
                if trading_day >= day_change:
                    # start1 = TRADETIME[security_ID]['day2']['open1']
                    end1 = TRADETIME[security_ID]['day2']['close1']
                    start2 = TRADETIME[security_ID]['day2']['open2']
                    # end2 = TRADETIME[security_ID]['day2']['close2']

            return [(day + pd.to_timedelta(end1),
                     day + pd.to_timedelta(start2))]
        else:
            assert False, "Not support NIGHT_TYPE yet"
    else:
        return [(day, day + pd.to_timedelta('9:30:00')),
                (day + pd.to_timedelta('11:30:00'),
                 day + pd.to_timedelta('13:00:00'))]


def _tick2bar(symbol, tick_data, freq):
    """ Transform tick data into bar data.
    """
    column_list = []
    time_type = None
    for name, col in tick_data.iteritems():
        if name in ['volume', 'turnover']:
            col_df = col.resample(freq).sum()
            # If not all elements are nan, fill nan with 0.
            if not col_df.isnull().all():
                col_df.fillna(0, inplace=True)
        elif name == 'price':
            col_df = col.resample(freq).ohlc()
            closes = col_df['close'].fillna(method='pad')
            col_df = col_df.apply(lambda x: x.fillna(closes))
        # TODO(reed): Using last value isn't suitable for all other
        # columns, but for Futures it's enough now. CHECK IT LATER.
        else:
            col_df = col.resample(freq).last().fillna(method='pad')
            # Use to distinct day or night.
            if name == 'type':
                time_type = col.iloc[0]

        column_list.append(col_df)

    # Concat all columns.
    bar_data = pd.concat(column_list, axis=1)

    # Filter data according to the trading time.
    first_time = tick_data.index[0]
    today = first_time.normalize()
    if time_type is None:
        time_type = NIGHT_TYPE if first_time.hour > 15 else DAY_TYPE
    rest_time_list = _get_rest_time(symbol, today, time_type)
    # NOTE(reed): All columns share the same index, so we just use the last
    # col to generate index.
    for start, end in rest_time_list:
        bar_data.drop(
            bar_data.index[(bar_data.index >= start) & (bar_data.index < end)],
            inplace=True)

    return bar_data


def get_day_bar(symbol, days, freq='1T', columns=DEFAULT, merge=True,
                data_source=ZHONGXIN):
    """Get bar data (k-lines) of specific symbol, days and frequency etc.

    This method fetch bar data of specific days. It receives similar parameters
    with :meth:`get_day_tick` method, and has an particular parameter `freq`,
    which assign the frequency of bar data.

    In order to see how to set 'freq', please refer to:
    http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

    Some frequently-used freq are:
        L, ms   milliseconds
        S       secondly frequency
        T, min  minutely frequency
        H       hourly frequency
        B       business day frequency
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency

    Args:
        symbol(str): Symbol of securities.
        days(int, str, pair of int, pair of str, list of int or list of str):
            Date or date range for data. when it's single int or str, it means
            the specific day; when it's pair of days, like ``(day1, day2)``,
            it means date range from ``day1`` to ``day2``, with ``day1`` and
            ``day2`` including; otherwise when it's list of days, like
            ``[day1, day2, day3]``, it means discrete days ``day1``, ``day2``
            and ``day3``.
        freq(str): Time frequency for k-lines, like ``1S``, ``5T`` etc.
        columns(list of str): Data columns to get, like ``price``, ``volume``
            etc.
        merge(bool): When ``freq`` is inner-day frequency, ``merge`` controls
            whether to merge data from each days; otherwise when ``freq`` is
            beyond inner-day frequency, like day, week or month frequency,
            this parameter MAKES NO SENSE.
        data_source(str): Data source, ZHONGXIN or YINHE.

    Returns:
        DataFrame or list of DataFrame: DataFrame containing all bar data or
            list of DataFrame, each DataFrame in the list for one day.

    .. seealso::
        See :meth:`get_day_tick` for tick data.
    """

    symbol = symbol.upper()
    # Get tick data first.
    tick_data_list = get_day_tick(symbol, days, columns=columns, merge=False,
                                  data_source=data_source)
    if tick_data_list is None:
        return None

    dts = pd.date_range('19700101', periods=2, freq=freq)
    delta = (dts[1] - dts[0]).total_seconds()
    # Inner-day frequency
    if delta < 86400:
        res = []
        if len(tick_data_list) < 5:
            for tick_data in tick_data_list:
                bar_data = _tick2bar(symbol, tick_data, freq)
                res.append(bar_data)
        else:
            pool = mp.Pool(processes=process_num)
            for tick_data in tick_data_list:
                res.append(pool.apply_async(_tick2bar,
                                            (symbol, tick_data, freq)))
            pool.close()
            pool.join()

            res = map(lambda ret: ret.get(), res)

        if merge:
            res = pd.concat(res)
    # Beyond day frequency.
    else:
        tick_data = pd.concat(tick_data_list)
        res = _tick2bar(symbol, tick_data, freq)
        res.dropna(inplace=True)

    return res


def _extract_contract_time(timestr, symbol):
    pat = re.compile(
        r'(\d{8})-{0,1}((\d{2}):(\d{2}):(\d{2})|(\d{2}):(\d{2})|(\d{2})|$)')
    try:
        time_list = pat.search(timestr).groups()
    except Exception, ee:
        logger.error(str(ee))
        return None, None
    ret_date = int(time_list[0])
    if not time_list[1]:
        res_time = TRADETIME[symbol]['day']['open1']
    else:
        if time_list[2]:
            res_time = ':'.join([e.zfill(2) for e in time_list[2:5]])
        if time_list[5]:
            res_time = time_list[5].zfill(2)+':'+time_list[6].zfill(2)+':00'
        if time_list[7]:
            res_time = time_list[7].zfill(2)+':00:00'
    return ret_date, res_time


def get_data_bar():
    pass


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# this is a important function
def _decode_tick_data(infoFrame, columns, pad=False):
    if infoFrame.empty:
        return None

    # Check the validation of columns.
    illegal_column_set = set(columns) - COLUMNS_SET
    if len(illegal_column_set):
        logger.error('illegal columns: %s', tuple(illegal_column_set))
        return None

    expand_columns = list(columns)

    if 'volume' in columns and 'acc_volume' not in columns:
        expand_columns.append('acc_volume')
    if 'turnover' in columns and 'acc_turnover' not in columns:
        expand_columns.append('acc_turnover')

    result = []
    base = [-1] * len(expand_columns)
    # instrument_id, TradingDay, content, type
    # 重新构建PRICE_LIST
    local_price_list = [e for e in expand_columns if e in PRICE_LIST]
    for i, element in infoFrame.iterrows():
        instrument_id = element['InstrumentID']
        time_type = element['Type']
        zipinfo = element['content']
        day_info = tp.TickList()
        buf = StringIO(zipinfo)
        with gzip.GzipFile(mode='rb', fileobj=buf) as gf:
            zipinfo = gf.read()
        day_info.ParseFromString(zipinfo)
        filedata = np.empty((len(day_info.tick), len(expand_columns)),
                            dtype=np.int64)
        time_list = np.empty((len(day_info.tick),), dtype=np.int32)
        for indd, info in enumerate(day_info.tick):
            base = [getattr(info, ele) if ele not in ['instrument_id', 'type']
                    and info.HasField(ele) else base[j]
                    for j, ele in enumerate(expand_columns)]
            filedata[indd] = base
            # Maintain time list.
            time_list[indd] = (getattr(info, 'time') if info.HasField('time')
                               else time_list[-1])

        if pad:
            # NOTE(reed): Fix wrong format time_list which affects padding,
            # like:
            #     9:00:00.000
            #     9:00:00.010
            #     9:00:01.000
            #     9:00:01.010
            #     ...
            #
            # After modification, it should be like:
            #     9:00:00.000
            #     9:00:00.500
            #     9:00:01.000
            #     9:00:01.500
            #     ...
            #
            # This algorithm is proposed by luyiming.

            second_list = np.empty((len(day_info.tick) + 1,), dtype=np.int32)
            milsecond_list = np.empty((len(day_info.tick) + 1,),
                                      dtype=np.int32)
            second_list[1:] = time_list % 100000 / 1000
            # NOTE(reed): We never touch the first time.
            second_list[0] = second_list[1] - 1

            milsecond_list[1:] = time_list % 100000
            milsecond_list[0] = milsecond_list[1]

            second_diff = second_list[1:] - second_list[:-1]
            milsecond_diff = milsecond_list[1:] - milsecond_list[:-1]

            wrong_time_indexes = np.all(
                np.stack([second_diff == 0, milsecond_diff < 500]), axis=0)

            # There are some timestamps need to be modified.
            if wrong_time_indexes.any():
                time_list[wrong_time_indexes] += (
                    500 - milsecond_diff[wrong_time_indexes])

                # NOTE(reed): This should be comment out when fully tested.
                assert np.all(time_list[1:] - time_list[:-1] >= 0)

        today = str(element['TradingDay'])
        tomorrow = (pd.Timestamp(today) + dtime.timedelta(days=1)) \
            .strftime('%Y%m%d')

        def translate_time(itime, today=today, tomorrow=tomorrow):
            """
            translate time from int to string
            """
            # print('%s type %s' % (itime, type(itime)))
            stime = str(int(itime)).zfill(9)
            stime = stime[0:2]+':'+stime[2:4]+':'+stime[4:6]+'.'+stime[6:]
            # if itime < 40000000:
            #     stime = tomorrow + ' ' + stime
            # else:
            #     stime = today + ' ' + stime
            stime = today + ' ' + stime
            # print stime
            try:
                return pd.Timestamp(stime)
            except:
                # print itime, today
                # 股票中有秒数超过60的现象
                return None
        df = pd.DataFrame(filedata, columns=expand_columns)
        # 将-1赋值为nan
        df[df == -1] = pd.np.nan

        # Set datetime and index.
        df['datetime'] = map(translate_time, time_list)
        df.set_index('datetime', inplace=True)

        if pad:
            is_futures = _is_futures(instrument_id)
            assert is_futures, "padding is not supported for stocks now."
            freq = '500ms'

            # TODO(reed): Using last value isn't suitable for all other
            # columns, but for Futures it's enough now. CHECK IT LATER.
            df = df.resample(freq).last().fillna(method='pad')

            # Filter data according to the trading time.
            first_time = df.index[0]
            today = first_time.normalize()
            rest_time_list = _get_rest_time(instrument_id, today, time_type)
            # NOTE(reed): All columns share the same index, so we just use the
            # last col to generate index.
            for start, end in rest_time_list:
                df.drop(
                    df.index[(df.index >= start) & (df.index < end)],
                    inplace=True)

        # 统一赋值instrument_id, 日夜盘标志与时间
        if 'instrument_id' in expand_columns:
            df['instrument_id'] = instrument_id
        if 'type' in expand_columns:
            df['type'] = time_type
        # NOTE(reed): volume and turnover should use acc_volume, acc_turnover
        # to calculate for tick data.
        # TODO(reed): Should we take the first acc_volume as the first volume?
        if 'volume' in expand_columns:
            df['volume'] = df['acc_volume'].diff().fillna(
                df['acc_volume'].iloc[0], limit=1)
        if 'turnover' in expand_columns:
            df['turnover'] = df['acc_turnover'].diff().fillna(
                df['acc_turnover'].iloc[0], limit=1)

        # 对所有的价格除以10000
        df[local_price_list] /= 10000

        result.append(df)

    return result

if __name__ == "__main__":
    print('begin')

    # 1.4. get_day_tick用法4：只传入期货类型代码表示获取“主力合约”
    print 'get t4'
    tt1 = time.time()
    t4 = get_day_tick(
        'if', [20140322, 20140323, 20140401],
        ['interest', 'instrument_id', 'type'],
        data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t4.instrument_id
    print t4.index[-1]

    # 1.5. get_day_tick用法5：只传入期货类型代码表示获取“主力合约”
    print 'get t5'
    tt1 = time.time()
    t5 = get_day_tick('if', (20140322, 20140326))
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t5.index[0], t5.instrument_id[0]
    print t5.index[-1]

    # 1.6. get_day_tick用法6：只传入期货类型代码表示获取“主力合约”, 取得数据大
    # 于4天,使用多进程.
    print 'get t6'
    tt1 = time.time()
    t6 = get_day_tick('if', (20140322, 20140426))
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t6.index[0], t6.instrument_id[0]
    print t6.index[-1]

    # 1.7. get_day_tick用法7：只传入期货类型代码表示获取“主力合约”, 取得数据大
    # 于4天,使用多进程, 并且对数据进行padding.
    print 'get t7'
    tt1 = time.time()
    t7 = get_day_tick('if', (20140322, 20140426), data_source=YINHE, pad=True)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t7.index[0], t7.instrument_id[0]
    print t7.index[-1]

    # 1.8. get_tick_data用法：传入一个“开始--终止”时间， 这里可以精确到毫秒
    #   返回该时间段的tick数据
    print 'get t8'
    tt1 = time.time()
    t8 = get_tick_data('if1601', '20160104-10:30', '20160105-10:30')
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t8.index[0], t8.instrument_id[0]
    print t8.index[-1]
    print len(t8)

    # 2.1. get_day_bar用法1: 取得分钟级k线数据
    print 'get b1'
    tt1 = time.time()
    b1 = get_day_bar('if', (20100416, 20100420), freq='1T', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b1.index[0], b1.instrument_id[0]
    print b1.index[-1]

    # 2.2. get_day_bar用法2: 取得5分钟级k线数据
    print 'get b2'
    tt1 = time.time()
    b2 = get_day_bar('if', (20100416, 20100420), freq='5T', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b2.index[0], b2.instrument_id[0]
    print b2.index[-1]

    # 2.3. get_day_bar用法3: 取得天级k线数据
    print 'get b3'
    tt1 = time.time()
    b3 = get_day_bar('if', (20140101, 20140131), freq='D', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b3.index[0], b3.instrument_id[0]
    print b3.index[-1]

    # 2.4. get_day_bar用法4: 取得周级k线数据
    print 'get b4'
    tt1 = time.time()
    b4 = get_day_bar('if', (20140101, 20140131), freq='W', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b4.index[0], b4.instrument_id[0]
    print b4.index[-1]

    # 2.5. get_day_bar用法5: 取得月级k线数据
    print 'get b5'
    tt1 = time.time()
    b5 = get_day_bar('if', (20140101, 20140331), freq='M', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b5.index[0], b5.instrument_id[0]
    print b5.index[-1]

    # 注： 返回的数据类型为pandas的DataFrame，其中column的字段在tick.proto文件
    #      中全部有标示。 不过返回值做了改动，有下列几点：
    #   1. 价格相关的都已经是真实的的价格--float型，不再是proto文件中的INT型
    #   2. time已经转换为pandas.Timestamp类型，并且包含了日期信息（20150102 10:30:25.332）
    #   3. proto中有些字段没有值(交易所没有提供), 全部用numpy模块的NaN替代
    #   4. 加了一个instrument_id字段（即合约号，如IF1601）
    #   5. 加了一个type字段表示日夜盘 0：日盘   1：夜盘
