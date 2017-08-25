from config import config
from psqldb import dbcon
import sys
import datetime

class user():
    #To check user credentials
    def do_login(self,username):
        select = "select * from dxads_sch.login where name='%s';" %username
        return dbcon().do_select(select=select)

    #To add user
    def add_user(self,username,pwd):
        valid_user = self.check_user_existance(username)
        if len(valid_user) == 0:
            insert = "insert into dxads_sch.login(name,password) values('%s','%s')" % (str(username), pwd)
            valid_insert =  dbcon().do_insert(insert=insert)
            if valid_insert is True:
                return self.__getID__(username)
            else:
                return "can not insert in database due to some technical error"
        else:
            return "user already exists!!!"

    def check_user_existance(self,username):
        select = "select name from dxads_sch.login where name='%s'" %username
        return dbcon().do_select(select=select)

    def __getEmail__(self,id):
        select = "select email from dxads_sch.profile where id=%d and init='1'" %id
        row = dbcon().do_select(select)
        if len(row) > 0:
            return row[0][0]
        else:
            return None

    def profile(self,fname,lname,gender,age,mobile,email):
        insert = "insert into dxads_sch.profile(id,fname,lname,gender,age,mobile,email,init) values(%d,'%s','%s','%s','%s','%s','%s','1');" % (
        config.__id__, fname, lname, gender, age, mobile, email)
        config.__email__ = email
        return dbcon().do_insert(insert)

    def __getID__(self,username):
        select = "select id from dxads_sch.login where name='%s'"% username
        row = dbcon().do_select(select)
        return row[0][0]

    def contact(self,message):
        insert = "insert into dxads_sch.contact(name,email,message,time) values('%s','%s','%s','%s');" % (config.__username__,config.__email__, message,self.currentdate())
        return dbcon().do_insert(insert)


    def getClientTableData(self):
        select = "select name from dxads_sch.tables;"
        tbl_name =  dbcon().do_select(select)

        data = [None] * len(tbl_name)

        for i in range(0, len(tbl_name)):
            for j in range(0, len(tbl_name[i])):
                select = "select * from dxads_sch.%s;"%tbl_name[i][j]
                data[i] = dbcon().do_select(select)

        return data

    def update_login(self,id):
        date = self.currentdate()
        insert = "update dxads_sch.login set last_login = '%s',status='0',live='1' where id=%d;" % (date,id)
        return dbcon().do_insert(insert)

    def update_logout(self,id):
        update = "update dxads_sch.login set live='0' where id=%d;"% id
        return dbcon().do_insert(update)


    def getProfileData(self,id):
        select = "select * from dxads_sch.profile where id=%d;" %id
        print select
        return dbcon().do_select(select)

    def getContactData(self):
        select = "select * from dxads_sch.contact;"
        return dbcon().do_select(select)

    def currentdate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def InactiveClient(self,cid):
        update = "update dxads_sch.login set active='0' where id=%d;" % cid
        print update
        return dbcon().do_insert(update)

    def updateClient(self,id,name,pwd,active,old_id):
        update = "update table dxads_sch.login set id=%d,name='%s',password='%s',active='%s' where id=%d"%(id,name,pwd,active,old_id)
        rslt = dbcon().do_insert(update)

        if rslt is True:
            update = "update table dxads_sch.profile set id=%d where id=%d ;" % (old_id,id)
            return dbcon().do_insert(update)

    def updateProfile(self,fname,lname,gender,id,age,mobile,email):
        update = "update table dxads_sch.profile set fname='%s',lname='%s',gender='%s',age=%d,mobile=%d email='%s' where id=%d" % (
        fname,lname,gender,age,mobile,email,id)

        return dbcon().do_insert(update)

if __name__ == "__main__":
    user()