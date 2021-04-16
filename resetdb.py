from maildao import MailDao
from mail import Mail
from userdao import UserDao
from user import User
import os
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(filename='output.log',format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

os.remove('users.db')
dao = UserDao()
dao.populate()
users = dao.selectAll()
for user in users:
    print (user.toString())

os.remove('mails.db')
dao = MailDao()
dao.populate()
mails = dao.selectAll()
for mail in mails:
    print(mail.ident,mail.sender,mail.subject)



