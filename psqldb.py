import psycopg2 as db
import sys


class dbcon(object):
    global con
    con = db.connect(dbname='dxads', host='localhost', user='dxads', password='root')
    global cursor
    cursor = con.cursor()

    def do_select(self,dbselect):



        cursor.execute(dbselect)
        row = cursor.fetchall()

        return row

    def do_insert(self,dbinsert):
        cursor.execute(dbinsert)
        con.commit()
        return True


    
if __name__ == "__main__":
    dbcon()