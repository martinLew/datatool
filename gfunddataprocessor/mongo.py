import pymongo as po

from globallogger import logger


class MongoDB:

    def __init__(self, user='reader', password='123456'):
        self.client = client = po.MongoClient()
        # db = client['admin']
        # try:
        #     db.authenticate(user, password)
        # except Exception, e:
        #     logger.error(str(e))
        #     return None

    def __del__(self):
        self.client.close()
