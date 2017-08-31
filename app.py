from __future__ import with_statement
from flask import (Flask, session, redirect, url_for,render_template, flash, request, make_response)
import os,numbers
from user import user
from master import master
from config import config


app = Flask(__name__)
app.config['SECRET_KEY'] = 'DIGITAL MARKETING!'


global user_obj
user_obj = user()

#------------------Front End--------------------
#-------------------loginpage------------------------------
@app.route('/')
def rtlogin():
    data = {'title': 'Digital Marketing | Login'}
    return render_template('master/login.html',**data)


@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        row = user_obj.do_login(username=request.form['un_txt'])
        if request.form['un_txt'] is None or request.form['pwd_txt'] is None:
            flash(message='Invalid Username or Password.')
            return redirect(url_for('rtlogin'))
        elif row[0][1] == request.form['un_txt'] :
            if row[0][2] == request.form['pwd_txt']:
                if user_obj.update_login(row[0][0]) is True and row[0][5] is True:
                    print "login==master"
                    master.__username__ = request.form['un_txt']
                    master.__id__ = user().__getID__(master.__username__)
                    if user().update_login(master.__id__) is True:
                        session['logged_in'] = 1
                        return redirect(url_for('rtmindex'))
                else:
                    session['logged_in'] = 1
                    config.__id__ = row[0][0]
                    config.__username__ = row[0][1]
                    config.__email__ = user_obj.__getEmail__(row[0][0])
                    return redirect(url_for('rtindex'))
            else:
                flash(message='Password Does not match.')
                return redirect(url_for('rtlogin'))
        else:
            flash(message='Invalid username')
            return redirect(url_for('rtlogin'))


#------------------regpage-----------------------------
@app.route('/registration',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        flag = False
        username = request.form['un_txt']
        pwd = request.form['pwd_txt']
        cpwd = request.form['cpwd_txt']

        if request.form['un_txt'] and request.form['pwd_txt'] and request.form['cpwd_txt'] is not None:
            if pwd != cpwd :
                flash(message='Password does not match.')
                return render_template('client/registration.html')
            else:
                error_msg = user_obj.add_user(username=username, pwd=pwd)
                session['logged_in'] = 1

                if isinstance(error_msg,basestring) is True:
                    flash(message=error_msg)
                elif isinstance(error_msg,numbers.Integral) is True:
                    config.__id__ = error_msg
                    config.__username__ = username
                    config.__email__ = None
                return redirect(url_for('rtprofile'))

        else:
            flash(message='Enter valid data.')
            return render_template('client/registration.html')

#------------------------cindexpage---------
@app.route('/index')
def rtindex():
    data = {'title': 'Client | Home'}
    username = config.__username__
    return render_template('client/index.html',username=username,**data)

#-----------------------profilepage--------------
@app.route('/profile')
def rtprofile():
    data = {'title': 'Client | Profile'}
    row = user_obj.getProfileData(config.__id__)
    if row is None:
        return render_template('client/profile.html',udata=0,username=config.__username__,**data)
    else:
        return render_template('client/profile.html', udata=row, username=config.__username__, **data)


@app.route('/profile',methods=['GET','POST'])
def update_profile():
    if request.method == "POST":
        flag = False
        fname = request.form['fname_txt']
        lname = request.form['lname_txt']
        age = request.form['age_nbtn']
        mobile = request.form['mobile_txt']
        email = request.form['email_txt']
        gender = True

        if request.form['gender_rbtn'] is 'True':
            gender = True
        elif request.form['gender_rbtn'] == False:
            gender = False

        flag = user_obj.profile(config.__id__,fname=fname,lname=lname,gender=gender,age=age,mobile=mobile,email=email)

        if flag is True:
            flash(message='Profile updated successfully.')
            return redirect(url_for('rtprofile'))
        elif flag is False:
            flash(message='Currently this service is not available')
            return redirect(url_for('rtprofile'))


#----------------contactpage-------
@app.route('/contact')
def rtcontact():
    data = {'title': 'Client | Contact'}
    return render_template('client/contact.html',username=config.__username__,email=config.__email__,**data)


@app.route('/contact',methods=['GET','POST'])
def reg_contact():
    if request.method == "POST":
        flag = False

        if request.form['message_txt'] is not None:
            flag = user_obj.contact(request.form['message_txt'])
        else:
            flash(message='Please enter message.')
            return render_template('client/contact.html')

        if flag is True:
            flash(message='inserted successfully.')
            return redirect(url_for('rtcontact'))


#---------------logoutpage--------------
@app.route('/logout')
def logout():
    if user_obj.update_logout(config.__id__) is True :
        session['logged_in'] = 0
        flash(message='You were logged out')
        del config.__id__, config.__email__, config.__username__
        return redirect(url_for('rtlogin'))


#-----------------backend-------------------------
#-----------------mindexpage----------------------
@app.route('/master/')
def rtmindex():
    title = "Master | Home"
    contact = user_obj.getContactData()
    chat = master().getChatData()
    return render_template('/master/index.html', username=master.__username__,contact=contact,chat=chat,title=title)


@app.route('/master/',methods=['GET','POST'])
def rtmchat():
    if request.method == 'POST':
        print request.form['msg_txt']
        if request.form['msg_txt'] is not None:
            if master().addChat(request.form['msg_txt']):
                return redirect(url_for('rtmindex'))


#----------------tablepage------------
@app.route('/master/tables')
def rtmtables():
    title = "Master | Tables"
    return render_template('/master/Table/tables.html',username=master.__username__, title=title)


#-----------tblloginpage-------------
#-------------------client data manipulation -------------------------
#-------------------client login data manipulation---------------------
@app.route('/master/login')
def rtclient():
    title = "Master | Login"
    data = user().getClientTableData(1)
    return render_template('/master/Table/tbl_login.html', username=master.__username__, title=title, data=data)


@app.route('/master/login/active',methods=['POST'])
def active():
    if request.method == 'POST':
        id = request.form['id']
        rslt = user_obj.ActiveClient(id)
        return redirect(url_for('rtclient'))


@app.route('/master/login/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        rslt = user_obj.InactiveClient(id)
    return redirect(url_for('rtclient'))


@app.route('/master/login/update',methods=['POST'])
def rtmupdate():
    if request.method == 'POST':
        id = request.form['id']
        title ='Master | Login | Update'
        data = user_obj.getLoginData(id)
        return render_template('/master/Table/loginform.html', username=master.__username__,id=id ,data=data,title=title)


@app.route('/master/login/Success',methods=['POST'])
def update():
    old_id = request.form['old_id']
    if request.method == 'POST':
        new_id = request.form['id']
        name = request.form['name']
        pwd = request.form['password']
        active = request.form['active']
        rslt = user().updateClient(new_id,name,pwd,active,old_id)
        return redirect(url_for('rtclient'))


#---------------masterpage-----------------
@app.route('/master/master')
def rtmdata():
    title = "Master | Master Data"
    data = master().getMasterTableData()
    return render_template('/master/Table/mdata.html',username=master.__username__,title=title,data=data)


#---------------tblprofilepage---------------------------
#---------------Client Profile Data Manipulation-------------------------------
@app.route('/master/profile')
def rtmtblprofile():
    title = "Master | Profile"
    data = user().getClientTableData(2)
    return render_template('/master/Table/tbl_profile.html', username=master.__username__, title=title, data=data)


@app.route('/master/profile/update',methods=['POST'])
def tblprofile():
    if request.method == 'POST':
        id = request.form['id']
        t = {'title':'Master | Profile | Update'}
        data = user_obj.getProfileData(id)
        print data
        return render_template('/master/Table/profileform.html', username=master.__username__,id=id ,data=data,**t)


@app.route('/master/profile/Success',methods=['POST'])
def UpdateProfile():
    old_id = request.form['old_id']
    if request.method == 'POST':
        new_id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']

        rslt = user().updateProfile(new_id,fname,lname,gender,age,mobile,email,old_id)
        return redirect(url_for('rtmtblprofile'))


@app.route('/test/')
def test():
    udata = user_obj.getProfileData(3)
    print udata;
    return render_template('/master/test.html',udata=udata)


#--------------mlogoutpage-----------------
@app.route('/master/logout')
def master_logout():
    if user().update_logout(master.__id__) is True:
        session['logged_in'] = 0
        flash(message='You were logger out')
        del master.__id__,master.__username__
        return redirect(url_for('rtlogin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)