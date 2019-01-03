import smtplib
import imaplib

#recognized keywords
keywords = ['suspend','restart', 'masterlock-stop','ping','force-poll']

#Theseservices do things in this order:
#1: log in to server and get ready to do stuff
#2: do requested process or action
#3: log out and close the box

#this will text a number with the desired text
def textUser(text):
    mail = smtplib.SMTP_SSL('smtp.gmail.com')
    mail.ehlo()
    mail.login('purplebotmail@gmail.com','purplemango1234')
    mail.sendmail('purplebotmail@gmail.com','5157243855@vtext.com',text)
    mail.close()

#this will look through the current emails in the folder, and
#look for keywords, if there are any requested, it will return
#a list of those keywords
def processEmails():
    global keywords
    msrvr = imaplib.IMAP4_SSL('imap.gmail.com',993)
    msrvr.login('purplebotmail@gmail.com','purplemango1234')
    keywordsFound = []
    msrvr.select('Inbox')
    typ, data = msrvr.search(None, 'ALL')
    #look at all emails in inbox
    for num in data[0].split():
        #get the text body
        typ, data = msrvr.fetch(num, '(UID BODY[TEXT])')
        #check for keywords
        for key in keywords:
            if key in str(data[0][1])[2:-5].lower().split():
                keywordsFound.append(key)
        #flag all emails for deletion
        msrvr.store(num, '+FLAGS', '\\Deleted')
    #expunge deleted inbox, close box, logout
    msrvr.expunge()
    msrvr.close()
    msrvr.logout()
    return(keywordsFound)
 
