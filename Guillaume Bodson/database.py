import sqlite3
import datetime
from sqlite3 import Error
from datetime import datetime

"""
Database class
Its purpose is to connect to the database file and through it add records to the database or fetch records from the database.
"""
class Database:

    def __init__(self):
        """
        Creates a connection to the database and creates the history table if it doesn't already exist
        :param self:
        :return:
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(r"database.db") #creates the connection to the sqlite3 database file
        except Error as e:
            print(e)

        if self.conn is not None:
            # create histroy table
            self.createTable()
        else:
            print("Error! cannot create the database connection.")


    def createTable(self):
        """ 
        create a table from the create_table_sql statement if it doesn't already exist
        :param self: 
        :return:
        """
        #sql statement
        sqlCreateHistoryTable = """ CREATE TABLE IF NOT EXISTS history (  
                                        id integer PRIMARY KEY,
                                        downloadSpeed text,
                                        uploadSpeed text,
                                        recordDatetime text
                                    ); """
        try:
            c = self.conn.cursor()
            c.execute(sqlCreateHistoryTable)
        except Error as e:
            print(e)

    def addRecord(self, downloadSpeed, uploadSpeed, curDatetime):
        """
        Create a new record into the history table
        :param self: 
        :param downloadSpeed: download speed
        :param uploadSpeed: upload speed
        :param curDatetime: date and time the information was saved
        :return: 
        """

        #gets the correct units for download and upload speed to make the data more readable
        downUnit = "MB"
        upUnit = "MB"
        if(downloadSpeed < 1):
            downloadSpeed *= 1000
            downUnit = "KB"
            if(downloadSpeed < 1):
                downloadSpeed *= 1000
                downUnit = "B"

        if(uploadSpeed < 1):
            uploadSpeed *= 1000
            upUnit = "KB"
            if(uploadSpeed < 1):
                uploadSpeed *= 1000
                upUnit = "B"

        downloadSpeed = str(downloadSpeed) + downUnit
        uploadSpeed = str(uploadSpeed) + upUnit
        record = (downloadSpeed, uploadSpeed, curDatetime)

        sql = ''' INSERT INTO history(downloadSpeed,uploadSpeed,recordDatetime)
                  VALUES(?,?,?) '''

        cur = self.conn.cursor()
        cur.execute(sql, record)
        self.conn.commit()

    def deleteAllRecords(self):
        """
        Deletes all rows in the history table
        :param self: 
        :return:
        """
        sql = 'DELETE FROM history'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def selectAllRecords(self):
        """
        Query all rows in the history table
        :param self:
        :return: array of rows of the table
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM history")

        rows = cur.fetchall()
        return rows
