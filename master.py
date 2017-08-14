from config import config
from psqldb import dbcon
import sys

class master():
    def do_login(self,username):
        select = "select * from master_sch.login where name='%s'" %username
        row = dbcon().do_select(select=select)

        if row[0][3] is True:
            print "Hello"
            return row
        else:
            return False



if __name__ == "__main__":
    master()