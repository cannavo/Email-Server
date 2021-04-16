class Mail:
    def __init__(self, ident, sender, reciever, subject, text, deletedInbox,deletedOutbox,date):
        self.ident = ident
        self.sender = sender
        self.reciever=reciever
        self.subject=subject
        self.text=text
        self.deletedInbox=deletedInbox
        self.deletedOutbox=deletedOutbox
        self.date=date

    
