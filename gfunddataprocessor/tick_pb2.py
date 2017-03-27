# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tick.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tick.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\ntick.proto\"\xc0\n\n\x04Tick\x12\x0c\n\x04time\x18\x01 \x01(\x05\x12\r\n\x05price\x18\x02 \x01(\x05\x12\x0e\n\x06volume\x18\x03 \x01(\x03\x12\x10\n\x08turnover\x18\x04 \x01(\x03\x12\x13\n\x0bmatch_items\x18\x05 \x01(\x05\x12\x10\n\x08interest\x18\x06 \x01(\x05\x12\x12\n\ntrade_flag\x18\x07 \x01(\x05\x12\x0f\n\x07\x62s_flag\x18\x08 \x01(\x05\x12\x12\n\nacc_volume\x18\t \x01(\x03\x12\x14\n\x0c\x61\x63\x63_turnover\x18\n \x01(\x03\x12\x0c\n\x04high\x18\x0b \x01(\x05\x12\x0b\n\x03low\x18\x0c \x01(\x05\x12\x0c\n\x04open\x18\r \x01(\x05\x12\x11\n\tpre_close\x18\x0e \x01(\x05\x12\x0e\n\x06settle\x18\x0f \x01(\x05\x12\x10\n\x08position\x18\x10 \x01(\x05\x12\x11\n\tcur_delta\x18\x11 \x01(\x05\x12\x12\n\npre_settle\x18\x12 \x01(\x05\x12\x15\n\rpre_positioin\x18\x13 \x01(\x05\x12\x12\n\nask_price1\x18\x14 \x01(\x05\x12\x12\n\nask_price2\x18\x15 \x01(\x05\x12\x12\n\nask_price3\x18\x16 \x01(\x05\x12\x12\n\nask_price4\x18\x17 \x01(\x05\x12\x12\n\nask_price5\x18\x18 \x01(\x05\x12\x12\n\nask_price6\x18\x19 \x01(\x05\x12\x12\n\nask_price7\x18\x1a \x01(\x05\x12\x12\n\nask_price8\x18\x1b \x01(\x05\x12\x12\n\nask_price9\x18\x1c \x01(\x05\x12\x13\n\x0b\x61sk_price10\x18\x1d \x01(\x05\x12\x13\n\x0b\x61sk_volume1\x18\x1e \x01(\r\x12\x13\n\x0b\x61sk_volume2\x18\x1f \x01(\r\x12\x13\n\x0b\x61sk_volume3\x18  \x01(\r\x12\x13\n\x0b\x61sk_volume4\x18! \x01(\r\x12\x13\n\x0b\x61sk_volume5\x18\" \x01(\r\x12\x13\n\x0b\x61sk_volume6\x18# \x01(\r\x12\x13\n\x0b\x61sk_volume7\x18$ \x01(\r\x12\x13\n\x0b\x61sk_volume8\x18% \x01(\r\x12\x13\n\x0b\x61sk_volume9\x18& \x01(\r\x12\x14\n\x0c\x61sk_volume10\x18\' \x01(\r\x12\x12\n\nbid_price1\x18( \x01(\x05\x12\x12\n\nbid_price2\x18) \x01(\x05\x12\x12\n\nbid_price3\x18* \x01(\x05\x12\x12\n\nbid_price4\x18+ \x01(\x05\x12\x12\n\nbid_price5\x18, \x01(\x05\x12\x12\n\nbid_price6\x18- \x01(\x05\x12\x12\n\nbid_price7\x18. \x01(\x05\x12\x12\n\nbid_price8\x18/ \x01(\x05\x12\x12\n\nbid_price9\x18\x30 \x01(\x05\x12\x13\n\x0b\x62id_price10\x18\x31 \x01(\x05\x12\x13\n\x0b\x62id_volume1\x18\x32 \x01(\r\x12\x13\n\x0b\x62id_volume2\x18\x33 \x01(\r\x12\x13\n\x0b\x62id_volume3\x18\x34 \x01(\r\x12\x13\n\x0b\x62id_volume4\x18\x35 \x01(\r\x12\x13\n\x0b\x62id_volume5\x18\x36 \x01(\r\x12\x13\n\x0b\x62id_volume6\x18\x37 \x01(\r\x12\x13\n\x0b\x62id_volume7\x18\x38 \x01(\r\x12\x13\n\x0b\x62id_volume8\x18\x39 \x01(\r\x12\x13\n\x0b\x62id_volume9\x18: \x01(\r\x12\x14\n\x0c\x62id_volume10\x18; \x01(\r\x12\x15\n\rask_avg_price\x18< \x01(\x05\x12\x15\n\rbid_avg_price\x18= \x01(\x05\x12\x18\n\x10total_ask_volume\x18> \x01(\x03\x12\x18\n\x10total_bid_volume\x18? \x01(\x03\x12\r\n\x05index\x18@ \x01(\x05\x12\x0e\n\x06stocks\x18\x41 \x01(\x05\x12\x0b\n\x03ups\x18\x42 \x01(\x05\x12\r\n\x05\x64owns\x18\x43 \x01(\x05\x12\x12\n\nhold_lines\x18\x44 \x01(\x05\"1\n\x08TickList\x12\x13\n\x04tick\x18\x01 \x03(\x0b\x32\x05.Tick\x12\x10\n\x08is_index\x18\x02 \x01(\x08')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TICK = _descriptor.Descriptor(
  name='Tick',
  full_name='Tick',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='Tick.time', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='price', full_name='Tick.price', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='volume', full_name='Tick.volume', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turnover', full_name='Tick.turnover', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='match_items', full_name='Tick.match_items', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interest', full_name='Tick.interest', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trade_flag', full_name='Tick.trade_flag', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bs_flag', full_name='Tick.bs_flag', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_volume', full_name='Tick.acc_volume', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_turnover', full_name='Tick.acc_turnover', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='high', full_name='Tick.high', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='low', full_name='Tick.low', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='open', full_name='Tick.open', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pre_close', full_name='Tick.pre_close', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='settle', full_name='Tick.settle', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='position', full_name='Tick.position', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cur_delta', full_name='Tick.cur_delta', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pre_settle', full_name='Tick.pre_settle', index=17,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pre_positioin', full_name='Tick.pre_positioin', index=18,
      number=19, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price1', full_name='Tick.ask_price1', index=19,
      number=20, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price2', full_name='Tick.ask_price2', index=20,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price3', full_name='Tick.ask_price3', index=21,
      number=22, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price4', full_name='Tick.ask_price4', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price5', full_name='Tick.ask_price5', index=23,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price6', full_name='Tick.ask_price6', index=24,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price7', full_name='Tick.ask_price7', index=25,
      number=26, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price8', full_name='Tick.ask_price8', index=26,
      number=27, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price9', full_name='Tick.ask_price9', index=27,
      number=28, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_price10', full_name='Tick.ask_price10', index=28,
      number=29, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume1', full_name='Tick.ask_volume1', index=29,
      number=30, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume2', full_name='Tick.ask_volume2', index=30,
      number=31, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume3', full_name='Tick.ask_volume3', index=31,
      number=32, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume4', full_name='Tick.ask_volume4', index=32,
      number=33, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume5', full_name='Tick.ask_volume5', index=33,
      number=34, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume6', full_name='Tick.ask_volume6', index=34,
      number=35, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume7', full_name='Tick.ask_volume7', index=35,
      number=36, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume8', full_name='Tick.ask_volume8', index=36,
      number=37, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume9', full_name='Tick.ask_volume9', index=37,
      number=38, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_volume10', full_name='Tick.ask_volume10', index=38,
      number=39, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price1', full_name='Tick.bid_price1', index=39,
      number=40, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price2', full_name='Tick.bid_price2', index=40,
      number=41, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price3', full_name='Tick.bid_price3', index=41,
      number=42, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price4', full_name='Tick.bid_price4', index=42,
      number=43, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price5', full_name='Tick.bid_price5', index=43,
      number=44, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price6', full_name='Tick.bid_price6', index=44,
      number=45, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price7', full_name='Tick.bid_price7', index=45,
      number=46, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price8', full_name='Tick.bid_price8', index=46,
      number=47, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price9', full_name='Tick.bid_price9', index=47,
      number=48, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_price10', full_name='Tick.bid_price10', index=48,
      number=49, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume1', full_name='Tick.bid_volume1', index=49,
      number=50, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume2', full_name='Tick.bid_volume2', index=50,
      number=51, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume3', full_name='Tick.bid_volume3', index=51,
      number=52, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume4', full_name='Tick.bid_volume4', index=52,
      number=53, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume5', full_name='Tick.bid_volume5', index=53,
      number=54, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume6', full_name='Tick.bid_volume6', index=54,
      number=55, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume7', full_name='Tick.bid_volume7', index=55,
      number=56, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume8', full_name='Tick.bid_volume8', index=56,
      number=57, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume9', full_name='Tick.bid_volume9', index=57,
      number=58, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_volume10', full_name='Tick.bid_volume10', index=58,
      number=59, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ask_avg_price', full_name='Tick.ask_avg_price', index=59,
      number=60, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid_avg_price', full_name='Tick.bid_avg_price', index=60,
      number=61, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_ask_volume', full_name='Tick.total_ask_volume', index=61,
      number=62, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_bid_volume', full_name='Tick.total_bid_volume', index=62,
      number=63, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='index', full_name='Tick.index', index=63,
      number=64, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stocks', full_name='Tick.stocks', index=64,
      number=65, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ups', full_name='Tick.ups', index=65,
      number=66, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='downs', full_name='Tick.downs', index=66,
      number=67, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hold_lines', full_name='Tick.hold_lines', index=67,
      number=68, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=1359,
)


_TICKLIST = _descriptor.Descriptor(
  name='TickList',
  full_name='TickList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tick', full_name='TickList.tick', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_index', full_name='TickList.is_index', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1361,
  serialized_end=1410,
)

_TICKLIST.fields_by_name['tick'].message_type = _TICK
DESCRIPTOR.message_types_by_name['Tick'] = _TICK
DESCRIPTOR.message_types_by_name['TickList'] = _TICKLIST

Tick = _reflection.GeneratedProtocolMessageType('Tick', (_message.Message,), dict(
  DESCRIPTOR = _TICK,
  __module__ = 'tick_pb2'
  # @@protoc_insertion_point(class_scope:Tick)
  ))
_sym_db.RegisterMessage(Tick)

TickList = _reflection.GeneratedProtocolMessageType('TickList', (_message.Message,), dict(
  DESCRIPTOR = _TICKLIST,
  __module__ = 'tick_pb2'
  # @@protoc_insertion_point(class_scope:TickList)
  ))
_sym_db.RegisterMessage(TickList)


# @@protoc_insertion_point(module_scope)
