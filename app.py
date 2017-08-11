from __future__ import with_statement
from flask import (Flask, session, redirect, url_for, abort,render_template, flash, request, make_response)
import os
from psqldb import dbcon


app = Flask(__name__)
app.config['SECRET_KEY'] = 'DIGITAL MARKETING!'


class dxads():
    '''
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")
    '''
    dbcon_obj = dbcon()
    select = "select * from dxads_sch.login"
    row = dbcon_obj.do_select(dbselect=select)
    id = row[0][0]
    username = row[0][1]
    email = "sr_mehta@itmusketeers.com"



global dx_obj
dx_obj = dxads()

@app.route('/')
def rtlogin():
    return render_template('client/login.html')


@app.route('/index')
def rtindex():
    return render_template('client/index.html')


@app.route('/login',endpoint='login', methods=['POST'])
def login():
    if request.method == 'POST':

        password = dx_obj.row[0][2]

        if dx_obj.username == request.form['un_txt'] and password == request.form['pwd_txt']:
            session['logged_in'] = 1
            return redirect(url_for('rtindex'))
        else:
            if request.form['un_txt'] is None or request.form['pwd_txt'] is None:
                flash(message='Invalid Username or Password.')
                return make_response(render_template('login.html'))



@app.route('/contact')
def rtcontact():
    return render_template('client/contact.html',username=dx_obj.username,email=dx_obj.email)


@app.route('/contact',methods=['GET','POST'])
def reg_contact():
    if request.method == "POST":
        flag = False
        insert = "insert into dxads_sch.contact(name,email,message) values('%s','%s','%s');" %(dx_obj.username,request.form['email_txt'],request.form['message_txt'])
        flag = dx_obj.dbcon_obj.do_insert(dbinsert=insert)

        if flag is True:
            flash(message='inserted successfully.')
            return render_template('client/contact.html')


@app.route('/profile')
def rtprofile():
    return render_template('client/profile.html')


@app.route('/profile',methods=['GET','POST'])
def update_profile():

    if request.method == "POST":
        flag = False
        fname = request.form['fname_txt']
        lname = request.form['lname_txt']
        age = request.form['age_nbtn']
        mobile = request.form['mobile_txt']
        email = request.form['email_txt']
        #init = True

        if request.form['gender_rbtn'] is False:

            insert = "insert into dxads_sch.profile(id,fname,lname,gender,age,mobile,email,init) values(%d,'%s','%s','0','%s','%s','%s','0');" %(dx_obj.id,fname,lname,age,mobile,email)
        else:
            insert = "insert into dxads_sch.profile(id,fname,lname,age,mobile,email,init) values(%d,'%s','%s','%s','%s','%s','0');" %(dx_obj.id, fname, lname, age, mobile, email)

        flag = dx_obj.dbcon_obj.do_insert(dbinsert=insert)


        if flag is True:
            flash(message='Successfully inserted in database!')
            return render_template('client/profile.html')
        elif flag is False:
            flash(message='Currently this service is not available')
            return render_template('client/profile.html')


@app.route('/logout')
def logout():
    session['logged_in'] = 0
    flash('You were logged out')
    return render_template('client/login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)