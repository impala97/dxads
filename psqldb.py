import psycopg2 as db
import sys


class dbcon():
    global con
    con = db.connect(dbname='dxads', host='localhost', user='dxads', password='root')
    global cursor
    cursor = con.cursor()

    def do_select(self,select):
        cursor.execute(select)

        row = cursor.fetchall()
        return row

    def do_insert(self,insert):
        cursor.execute(insert)
        con.commit()
        return True


if __name__ == "__main__":
    dbcon()