"""
操作数据库
"""
import os
import pymongo

class MongoDB:

    def __init__(self, db, coll):
        self.db = db
        self.coll = coll
        self.conn = self.get_connection()

    def get_connection(self):
        """
        获得一个mongo数据库的连接

        :param db:数据库名称
        :param coll:需要连接的集合
        :return:如果成功连接到数据库，则返回一个数据库连接，否则返回None
        """
        env_dict = os.environ
        try:
            mongo_data_uri = env_dict["MONGO_DAT_URI"]
            client = pymongo.MongoClient(mongo_data_uri)
            db = client[self.db]
            conn = db[self.coll]
            return conn
        except Exception as err:
            print(str(err))
            return None
    
    def insert_many(self, items):
        """
        将items批量添加到数据库中
        """
        try:
            self.conn.insert_many(items)
            return True
        except Exception as err:
            print(str(err))
            return False

def main():
    mongo = MongoOperate("testDB", "xdaili").conn
    # item = {"iport":"192.168.1.1:8888"}
    # mongo.add2db([item])
    result = mongo.find()
    for i in result:
        print(i)
    
if __name__ == "__main__":
    main()
