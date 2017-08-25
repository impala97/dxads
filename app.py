from __future__ import with_statement
from flask import (Flask, session, redirect, url_for,render_template, flash, request, make_response)
import os,numbers
from user import user
from master import master
from config import config


app = Flask(__name__)
app.config['SECRET_KEY'] = 'DIGITAL MARKETING!'

#------------------Front End--------------------

global user_obj
user_obj = user()


@app.route('/index')
def rtindex():
    data = {'title': 'Client | Home'}
    return render_template('client/index.html',**data)


@app.route('/')
def rtlogin():
    data = {'title': 'Client | Login'}
    return render_template('client/login.html',**data)


@app.route('/contact')
def rtcontact():
    data = {'title': 'Client | Contact'}
    return render_template('client/contact.html',username=config.__username__,email=config.__email__,**data)


@app.route('/profile')
def rtprofile():
    data = {'title': 'Client | Profile'}
    row = user_obj.getProfileData(config.__id__)
    print row
    return render_template('client/profile.html',udata=row,**data)


@app.route('/logout')
def logout():
    if user_obj.update_logout(config.__id__) is True :
        session['logged_in'] = 0
        flash(message='You were logged out')
        del config.__id__, config.__email__, config.__username__
        return render_template('client/login.html')


@app.route('/registration')
def rtregister():
    data = {'title': 'Client | Registration'}
    return render_template('client/registration.html',**data)


@app.route('/master/')
def rtmlogin():
    data = {'title' : 'Master | Login'}
    return render_template('/master/login.html',**data)


@app.route('/master/registration')
def rtmregister():
    return redirect('master/login.html')


@app.route('/master/index')
def rtmindex(operation=None):
    title = "Master | Home"
    contact = user_obj.getContactData()
    chat = master().getChatData()
    return render_template('/master/index.html', username=master.__username__,contact=contact,chat=chat,title=title)


@app.route('/master/index',methods=['GET','POST'])
def rtmchat():
    if request.method == 'POST':
        print request.form['msg_txt']
        if request.form['msg_txt'] is not None:
            if master().addChat(request.form['msg_txt']):
                return redirect(url_for('rtmindex'))


@app.route('/master/tables')
def rtmtables():
    title = "Master | Tables"
    return render_template('/master/Table/tables.html',username=master.__username__, title=title)


@app.route('/master/master')
def rtmdata():
    title = "Master | Master Data"
    data = master().getMasterTableData()
    return render_template('/master/Table/mdata.html',username=master.__username__,title=title,data=data)


@app.route('/master/logout')
def master_logout():
    if master().update_logout() is True:
        session['logged_in'] = 0
        flash(message='You were logger out')
        del config.__id__,config.__email__,config.__username__
        return url_for('rtmlogin')


#-------------------LoginPage------------------------------
@app.route('/login',endpoint='login', methods=['POST'])
def login():
    if request.method == 'POST':
        row = user_obj.do_login(username=request.form['un_txt'])

        if request.form['un_txt'] is None or request.form['pwd_txt'] is None:
            flash(message='Invalid Username or Password.')
            return render_template('client/login.html')
        elif row[0][1] == request.form['un_txt'] :
            if row[0][2] == request.form['pwd_txt']:
                if user_obj.update_login(row[0][0]) is True:
                    session['logged_in'] = 1
                    config.__id__ = row[0][0]
                    config.__username__ = row[0][1]
                    config.__email__ = user_obj.__getEmail__(row[0][0])
                    return redirect(url_for('rtindex'))
            else:
                flash(message='Password Does not match.')
                return render_template('client/login.html')
        else:
            flash(message='Invalid username')
            return render_template('client/login.html')



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


#---------------------ProfilePage------------------


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

        print "error"
        if request.form['gender_rbtn'] is 'True':
            print "error1"
            gender = True
        elif request.form['gender_rbtn'] == False:
            gender = False

        flag = user_obj.profile(fname=fname,lname=lname,gender=gender,age=age,mobile=mobile,email=email)

        if flag is True:
            flash(message='Profile updated successfully.')
            return render_template('client/profile.html')
        elif flag is False:
            flash(message='Currently this service is not available')
            return render_template('client/profile.html')


#------------------RegistrationPage-----------------------------
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
                print 'hello'
                error_msg = user_obj.add_user(username=username, pwd=pwd)
                session['logged_in'] = 1

                if isinstance(error_msg,basestring) is True:
                    flash(message=error_msg)
                elif isinstance(error_msg,numbers.Integral) is True:
                    config.__id__ = error_msg
                    config.__username__ = username
                    config.__email__ = None


                return render_template('client/index.html')

        else:
            flash(message='Enter valid data.')
            return render_template('client/registration.html')


#-----------------BackEnd-----------------------------------------
#-----------------login-------------------------------------------


@app.route('/master/',methods=['GET','POST'])
def master_login():

    if request.method == 'POST' :
        row = master().do_login(username=request.form['un_txt'])

        if row is False:
            flash(message='User Does not exist.')
            return render_template('master/login.html')

        if request.form['un_txt'] is None or request.form['pwd_txt'] is None :
            flash(message='Invalid Username or Password.')
            return render_template('master/login.html')
        elif row[0][1] == request.form['un_txt'] :
            if row[0][2] == request.form['pwd_txt']:
                master.__username__ = request.form['un_txt']
                master.__id__ = master().__getId__()
                print master.__username__
                if master().update_login() is True:
                    session['logged_in'] = 1
                    return redirect(url_for('rtmindex'))
            else:
                flash(message='Password Does not match.')
                return render_template('master/login.html')
        else:
            flash(message='Invalid username')
            return render_template('master/login.html')

#----------------------Registration--------------


@app.route('/master/registration',methods=['GET','POST'])
def master_register():
    if request.method == 'POST':
        flag = False
        username = request.form['un_txt']
        pwd = request.form['pwd_txt']
        cpwd = request.form['cpwd_txt']
        email = request.form['email_txt']

        if request.form['un_txt'] and request.form['email_txt'] and request.form['pwd_txt'] and request.form['cpwd_txt'] is not None:
            if pwd != cpwd :
                flash(message='Password does not match.')
                return render_template('master/login.html')
            else:
                error_msg = master().add_master(username, pwd, email)

                print error_msg
                if isinstance(error_msg,basestring) is True:
                    flash(message=error_msg)
                else:
                    session['logged_in'] = 1
                return redirect(url_for('rtmlogin'))
        else:
            flash(message='Enter valid data.')
            return render_template('master/index.html')


#-------------------client data manipulation -------------------------
#-------------------client login data manipulation---------------------
@app.route('/master/login')
def rtclient():
    title = "Master | Client Data"
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
        t = {'title':'Master | Login | Update'}
        data = user_obj.getLoginData(id)
        return render_template('/master/Table/loginform.html', username=master.__username__,id=id ,data=data,**t)


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


#---------------Client Profile Data Manipulation-------------------------------
@app.route('/master/profile')
def rtmtblprofile():
    title = "Master | Client Profile Data"
    data = user().getClientTableData(2)
    return render_template('/master/Table/tbl_profile.html', username=master.__username__, title=title, data=data)


@app.route('/master/profile',methods=['POST'])
def tblprofile():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)