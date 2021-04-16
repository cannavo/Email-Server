import dataset
import logging
from user import User
from flask import current_app

class UserDao:
    def __init__(self):
        self.connectString = 'sqlite:///users.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['users']
        try:
            self.logger = current_app.logger
        except:
            self.logger = logging.getLogger('root')
        
    def rowToUser(self,row):
        user = User(row['userid'], row['password'])
        return user

    def userToRow(self,user):
        row = dict(userid=user.userid, password=user.password)
        return row

    def selectByUserId(self,userid):
        rows   = self.table.find_one(userid=userid)
        if (rows is None):
            return None
        else:
            return self.rowToUser(rows)

    def selectAll(self):
        rows   = self.table.all()
        result = []
        for row in rows:
            result.append(self.rowToUser(row))
        return result
        
    def insert(self,user):
        self.table.insert(self.userToRow(user))
        self.db.commit()

    def update(self,user):
        self.table.update(self.userToRow(user),['userid'])
        self.db.commit()

    def delete(self,user):
        self.table.delete(userid=userid)
        self.db.commit()

    def populate(self):
        self.table.insert(self.userToRow(User('nico','1234')))
        self.table.insert(self.userToRow(User('nicky','4321')))
        self.table.insert(self.userToRow(User('alex','password')))
        self.db.commit()
