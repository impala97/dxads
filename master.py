from psqldb import dbcon
import sys
from flask_wtf import form
import datetime


class master:
    __username__ = None
    __id__ = None

#-------------access after login-----------
    def do_login(self,username):
        select = "select * from master_sch.login where name='%s'" %username
        row = dbcon().do_select(select=select)

        if row[0][4] is True:
            return row
        else:
            return False

    def __getId__(self):
        select = "select id from master_sch.login where name='%s'"%master.__username__
        row = dbcon().do_select(select)
        print row[0][0]
        return row[0][0]

    def getMasterTableData(self):
        select = "select name from master_sch.tables;"
        tbl_name =  dbcon().do_select(select)

        data = [None] * len(tbl_name)

        for i in range(0, len(tbl_name)):
            for j in range(0, len(tbl_name[i])):
                select = "select * from master_sch.%s;"%tbl_name[i][j]
                data[i] = dbcon().do_select(select)
        return data

    def update_login(self):
        date  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        insert = "update master_sch.login set last_login = '%s',status='0',live='1' where id=%d;"%(date,master.__id__)
        return dbcon().do_insert(insert)

    def update_logout(self):
        update = "update master_sch.login set live='0' where id=%d" %self.__id__
        return dbcon().do_insert(update)

    #----------------access before login-------------------------
    #To add master
    def add_master(self,username,pwd,email):
        valid_user = self.check_master_existance(username)
        if len(valid_user) == 0:
            insert = "insert into master_sch.login(name,pwd,email) values('%s','%s','%s')" % (str(username), pwd,email)
            valid_insert =  dbcon().do_insert(insert=insert)
            if valid_insert is True:
                return self.__getId__()
            else:
                return "can not insert in database due to some technical error"
        else:
            return "user already exists!!!"

    def check_master_existance(self,username):
        select = "select name from master_sch.login where name='%s' and active='1'" %username
        return dbcon().do_select(select=select)

    def currentdate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def addChat(self,msg):
        insert = "insert into master_sch.chat(name,message,time) values('%s','%s','%s')"%(master.__username__,msg,self.currentdate())
        return dbcon().do_insert(insert)

    def getChatData(self):
        select = "select * from master_sch.chat;"
        return dbcon().do_select(select)

    def DeletebyId(self,id=0):
        delete = "delete * from "
if __name__ == "__main__":
    master()