from __future__ import with_statement
from flask import (Flask, session, redirect, url_for, abort,render_template, flash, request, make_response)
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
    return render_template('client/profile.html',**data)


@app.route('/logout')
def logout():
    session['logged_in'] = 0
    flash(message='You were logged out')
    del config.__id__, config.__email__, config.__username__
    return render_template('client/login.html')


@app.route('/registration')
def rtregister():
    data = {'title': 'Client | Registration'}
    return render_template('client/registration.html',**data)


@app.route('/master/index')
def rtmindex():
    data = {'title' : 'Master | Home'}
    return render_template('/master/index.html', **data)


@app.route('/master/registration')
def rtmregister():
    return redirect('master/login.html')


@app.route('/master/tables')
def rtmtables():
    data = {'title': 'Master | Tables'}
    return render_template('/master/tables.html',username=config.__username__,**data)


@app.route('/master/logout')
def master_logout():
    session['logged_in'] = 0
    flash(message='You were logger out')
    del config.__id__,config.__email__,config.__username__
    return url_for('rtmlogin')


@app.route('/master/')
def rtmlogin():
    return render_template('/master/login.html')

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
                session['logged_in'] = 1
                print row[0][0]
                config.__id__ = row[0][0]
                config.__username__ = row[0][1]
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
            return render_template('client/contact.html')


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
                session['logged_in'] = 1
                config.__id__ = row[0][0]
                config.__username__ = row[0][1]
                config.__email__ = row[0][3 ]
                return render_template('master/index.html',username=config.__username__)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)