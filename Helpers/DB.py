import mysql.connector
import os


class Connection:

    def __init__(self, *args):
        self.connection = None
        self.logging = args[0]
        # print(os.getenv('DB_PORT'))
        # exit()
        try:
            # dev
            self.connection = mysql.connector.connect(host='localhost',
                                               user='root',
                                               password='',
                                               database='netcost',
                                               port='3306')

            # prod
            # self.connection = mysql.connector.connect(host='217.76.58.30',
            #                                           user='forge',
            #                                           password='aEXgPiaa5Kfu1XKZMtym',
            #                                           database='netcost',
            #                                           port='3306')
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)

    def fetch_one(self, sql, where=None):
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(sql, where)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def fetchAll(self, sql, where=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, where)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def fetchMany(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchmany()
            cursor.close()
            return result
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def update(self, sql, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def insert(self, sql, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def insert_return_id(self, sql, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            id = cursor.lastrowid
            cursor.close()
            return id
        except Exception as Argument:
            self.logging.error("Exception occurred: " + str(Argument), exc_info=True)
            self.resetConnection()
            return False

    def resetConnection(self):
        self.connection.close()
        self.connection = mysql.connector.connect(host='localhost',
                                               user='root',
                                               password='',
                                               database='netcost',
                                               port='3306')
        # self.connection = mysql.connector.connect(host='217.76.58.30',
        #                                           user='forge',
        #                                           password='aEXgPiaa5Kfu1XKZMtym',
        #                                           database='netcost',
        #                                           port='3306')
