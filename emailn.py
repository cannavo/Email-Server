from flask import Flask
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
import logging
import sys
from logging.handlers import RotatingFileHandler
from logging import Formatter
from mail import Mail
from maildao import MailDao
from userdao import UserDao
from user import User
import datetime
from pytz import timezone

app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    valid=0
    if ('userid' in request.form):
        if (isValid(request.form["userid"],request.form["password"])==1):
            return redirect(url_for('inbox'))
        elif (isValid(request.form["userid"],request.form["password"])==2):
            valid=2 #incorrect password
        else:
            valid=3 #user not found 
    # the code below is executed if the credentials were invalid
    return render_template('login.html', **locals())

def isValid(userid, password):
    dao = UserDao()
    user = dao.selectByUserId(userid)
    if (user is None):
        return 3
    elif(user.password!=password):
        return 2
    else:
        session['userid']=user.userid
        session['mail']=None
        session['reply']=None
        return 1
    
@app.route('/create', methods=['POST', 'GET'])
def create():
    valid=0
    if ('userid' in request.form):
        if (isValidCreate(request.form['userid'],request.form['password1'],request.form['password2'])==1):
            createAccount(request.form['userid'],request.form['password1'])
            return redirect(url_for('login'))
        elif (isValidCreate(request.form['userid'],request.form['password1'],request.form['password2'])==2):
            valid=2 # passwords dont match
        else:
            valid=3 #user already exists
    # the code below is executed if the credentials were invalid
    return render_template('create.html', **locals())


def isValidCreate(userid, password1,password2):
    dao = UserDao()
    user = dao.selectByUserId(userid)
    if (user is not None):
        return 3
    elif(password1!=password2):
        return 2
    else:
        return 1
    
def createAccount(userid,password):
    user=User(userid,password)
    dao=UserDao()
    dao.insert(user)
        
@app.route('/inbox', methods=['POST', 'GET'])
def inbox():
    ident=request.form.get('ident',None)
    if(session['mail'] is not None):
        ident=session['mail']
    session['mail']=None
    dao=MailDao()
    mails=dao.selectInbox(session['userid'])
    mails.reverse()
    mail=dao.selectById(ident)
    length=dao.numInbox(session['userid'])
    if ('log' in request.form):
        session['userid']=None
        return redirect(url_for('login'))
    elif('delete' in request.form):
        deleteMailIn(request.form['delete'])
        return redirect(url_for('inbox'))
    elif('reply' in request.form):
        session['reply']=request.form['reply']
        return redirect(url_for('new'))
    return render_template('inbox.html', **locals())
        
def deleteMailIn(ident):
    dao=MailDao()
    mail=dao.selectById(ident)
    mail.deletedInbox=1
    dao.update(mail)
    
@app.route('/outbox', methods=['POST', 'GET'])
def outbox():
    ident=request.form.get('ident',None)
    if(session['mail'] is not None):
        ident=session['mail']
    session['mail']=None
    dao=MailDao()
    mails=dao.selectOutbox(session['userid'])
    mails.reverse()
    mail=dao.selectById(ident)
    length=dao.numInbox(session['userid'])
    if ('log' in request.form):
        session['userid']=None
        return redirect(url_for('login'))
    elif('delete' in request.form):
        deleteMailOut(request.form['delete'])
        return redirect(url_for('outbox'))
    return render_template('outbox.html', **locals())

def deleteMailOut(ident):
    dao=MailDao()
    mail=dao.selectById(ident)
    mail.deletedOutbox=1
    dao.update(mail)

@app.route('/trash', methods=['POST', 'GET'])
def trash():
    dao=MailDao()
    mails=dao.selectTrash(session['userid'])
    mails.reverse()
    mail=dao.selectById(request.form.get('ident',None))
    length=dao.numInbox(session['userid'])
    if ('log' in request.form):
        session['userid']=None
        return redirect(url_for('login'))
    elif('delete' in request.form):
        deleteMailTrash(request.form['delete'])
        return redirect(url_for('trash'))
    elif('reply' in request.form):
        session['reply']=request.form['reply']
        return redirect(url_for('new'))
    return render_template('trash.html', **locals())

def deleteMailTrash(ident):
    dao=MailDao()
    mail=dao.selectById(ident)
    mail.deletedInbox=2
    dao.update(mail)
    
@app.route('/new', methods=['POST', 'GET'])
def new():
    reciever=session['reply']
    session['reply']=None
    dao=MailDao()
    length=dao.numInbox(session['userid'])
    if('log' in request.form):
        session['userid']=None
        return login()
    elif('rec' in request.form):
        if(isValidUser(request.form['rec'])):
            num=dao.numMails()
            now=datetime.datetime.now(timezone('US/Eastern'))
            textMail=request.form['text']
            textMail=textMail.replace('\r\n','<br>')
            mail=Mail(num,session['userid'],request.form['rec'],request.form['subj'],textMail,0,0,now.strftime("%m/%d/%Y %H:%M"))
            dao.insert(mail)
            session['mail']=num
            return redirect(url_for('outbox'))
        else:
            num=dao.numMails()
            textMail=request.form['text']
            textMail=textMail.replace('\r\n','<br>')
            text="Mail you tried to send:<br>To: "+request.form['rec']+"<br>Subject: "+request.form['subj']+"<br>"+textMail
            now=datetime.datetime.now(timezone('US/Eastern'))
            mail=Mail(num,'System',session['userid'],"User doesn't exist",text,0,0,now.strftime("%m/%d/%Y %H:%M"))
            dao.insert(mail)
            session['mail']=num
            return redirect(url_for('inbox'))
    return render_template('new.html', **locals())    
            
def isValidUser(userid):
    dao=UserDao()
    user=dao.selectByUserId(userid)
    if(user is None):
        return False
    return True

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    streamhandler = logging.StreamHandler(sys.stderr)
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(Formatter("[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"))
    app.logger.addHandler(streamhandler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0')
