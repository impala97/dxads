from config import config
from psqldb import dbcon
import sys

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
                return self.__getIdbyName__(username=username)
            else:
                return "can not insert in database due to some technical error"
        else:
            return "user already exists!!!"

    def check_user_existance(self,username):
        select = "select name from dxads_sch.login where name='%s'" %username
        return dbcon().do_select(select=select)

    def __getIdbyName__(self,username):
        select = "select id from dxads_sch.login where name = '%s';",username
        row = dbcon().do_select(select=select)
        print row
        return row[0][0]

    def __getEmailbyId__(self,id):
        select = "select email from dxads_sch.profile where id=%d"%id
        return dbcon().do_select(select)

    def profile(self,fname,lname,gender,age,mobile,email):
        insert = "insert into dxads_sch.profile(id,fname,lname,gender,age,mobile,email,init) values(%d,'%s','%s','%s','%s','%s','%s','1');" % (
        config.__id__, fname, lname, gender, age, mobile, email)

        config.__email__ = email
        return dbcon().do_insert(insert=insert)

    def __getID__(self):
        select = "select id from dxads_sch.login where name='%s'"%config.__username__
    def contact(self,message):
        insert = "insert into dxads_sch.contact(name,email,message) values('%s','%s','%s');" % (config.__username__,email, message)
        return dbcon().do_insert(dbinsert=insert)



if __name__ == "__main__":
    user()