from psqldb import dbcon
import sys

class master():
    def do_login(self,username):
        select = "select * from master_sch.login where name='%s'" %username
        row = dbcon().do_select(select=select)

        if row[0][4] is True:
            return row
        else:
            return False

    #To add master
    def add_master(self,username,pwd,email):
        valid_user = self.check_master_existance(username)
        if len(valid_user) == 0:
            insert = "insert into master_sch.login(name,pwd,email) values('%s','%s','%s')" % (str(username), pwd,email)
            valid_insert =  dbcon().do_insert(insert=insert)
            if valid_insert is True:
                return self.__getId__(username)
            else:
                return "can not insert in database due to some technical error"
        else:
            return "user already exists!!!"

    def check_master_existance(self,username):
        select = "select name from master_sch.login where name='%s' and active='1'" %username
        return dbcon().do_select(select=select)

    def __getId__(self,username):
        select = "select id from master_sch.login where name='%s'"%username
        row = dbcon().do_select(select)
        return row[0][0]


if __name__ == "__main__":
    master()