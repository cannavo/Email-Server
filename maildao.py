import dataset
import logging
from mail import Mail
from flask import current_app

class MailDao:
    def __init__(self):
        self.connectString = 'sqlite:///mails.db'
        self.db=dataset.connect(self.connectString)
        self.table=self.db['mails']
        try:
            self.logger=current_app.logger
        except:
            self.logger=logging.getLogger('root')
        
    def readMails(self):
        rows=self.table.all()
        result = []
        for row in rows:
            result.append(self.rowToMail(row))
        return result
                
    def rowToMail(self,row):
        mail = Mail(row['ident'], row['sender'],row['reciever'],row['subject'],row['text'],row['deletedInbox'],row['deletedOutbox'],row['date'])
        return mail

    def mailToRow(self,mail):
        row = dict(ident=mail.ident,sender=mail.sender,reciever=mail.reciever,subject=mail.subject,text=mail.text,deletedInbox=mail.deletedInbox,deletedOutbox=mail.deletedOutbox,date=mail.date)
        return row

    
    def selectById(self,ident):
        if(ident is None):
            return None
        else:
            return self.rowToMail(self.table.find_one(ident=ident))

    def selectInbox(self,reciever):
        result=[]
        if(self.table.find_one(reciever=reciever,deletedInbox=0) is not None):
            mails  = self.table.find(reciever=reciever,deletedInbox=0)
            for mail in mails:
                result.append(self.rowToMail(mail))
        return result 
            
    def selectOutbox(self,sender):
        result=[]
        if(self.table.find_one(sender=sender,deletedOutbox=0) is not None):
            mails  = self.table.find(sender=sender,deletedOutbox=0)
            for mail in mails:
                result.append(self.rowToMail(mail))
        return result
    
    def selectTrash(self,reciever):
        result=[]
        if(self.table.find_one(reciever=reciever,deletedInbox=1) is not None):
            mails  = self.table.find(reciever=reciever,deletedInbox=1)
            for mail in mails:
                result.append(self.rowToMail(mail))
        return result
    
    def selectAll(self):
        result = self.readMails()
        return result
        
    def insert(self,mail):
        self.table.insert(self.mailToRow(mail))
        self.db.commit()

    def update(self,mail):
        self.table.update(self.mailToRow(mail),['ident'])
        self.db.commit()
        
    def numMails(self):
        mails = self.readMails()
        return len(mails)
    
    def numInbox(self, userid):
        mails=self.selectInbox(userid)
        return len(mails)
    
    def populate(self):
        self.table.insert(self.mailToRow(Mail(0,'nico','alex','Hi','Hello My friend',0,0,'02/28/2018 00:30')))
        self.table.insert(self.mailToRow(Mail(1,'nico','alex','Hello','Where have you been al this time',0,0,'02/28/2018 01:30')))
        self.table.insert(self.mailToRow(Mail(2,'nico','nicky','How are you?','I miss you',0,0,'02/28/2018 02:30')))
        self.table.insert(self.mailToRow(Mail(3,'nico','nicky','Bye','When are you coming to see me',0,0,'02/28/2018 03:30')))
        self.table.insert(self.mailToRow(Mail(4,'nico','nicky','Hi There','Want to go out next week?',0,0,'02/28/2018 04:30')))
        self.table.insert(self.mailToRow(Mail(5,'nicky','alex','Where?','Where do you want to meet',0,0,'02/28/2018 05:30')))
        self.table.insert(self.mailToRow(Mail(6,'nicky','alex','How?','How did you do that?',0,0,'02/28/2018 06:30')))
        self.table.insert(self.mailToRow(Mail(7,'nicky','alex','When?','When are we going to the movies',1,0,'02/28/2018 07:30')))
        self.table.insert(self.mailToRow(Mail(8,'nicky','nico','Greetings','Greeting my friend',0,0,'02/28/2018 08:30')))
        self.table.insert(self.mailToRow(Mail(9,'nicky','nico','Why?','Why are you like that',0,0,'02/28/2018 09:30')))
        self.table.insert(self.mailToRow(Mail(10,'alex','nico','Hello','Hello Hello are you gonna answer',0,0,'02/28/2018 10:30')))
        self.table.insert(self.mailToRow(Mail(11,'alex','nicky','Where are you?','Where are you I cant see you',0,0,'02/28/2018 11:30')))
        self.table.insert(self.mailToRow(Mail(12,'alex','nicky','Bye Bye','Bye bye ill never see you again',0,0,'02/28/2018 12:30')))
        self.table.insert(self.mailToRow(Mail(13,'alex','nico','Ohh','Ohh that is sad',0,0,'02/28/2018 13:30')))
        self.table.insert(self.mailToRow(Mail(14,'alex','nico','That is wrong','That is wrong you should never do that',0,0,'02/28/2018 14:30')))
