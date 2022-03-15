import pymysql

class Connector:

    def connect_db(self, dbName):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='2642805', db=dbName, charset='utf8')
        return db