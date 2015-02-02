import requests
#Currently this test module will make repeated communications with server, but for final version
#I need to make the self.init only time that it connects to server, than gets all the pages needed
#And saves that data to a textfile or something, the data can be processed form that later!
class Seraph(object):

    def __init__(self, username, password):
        a = requests.session()
        b = dict(username=username,password=password)
        self.eID = a.post('https://angel.starkstate.edu/signon/authenticate.asp', data=b) #self.eId is the error code recieved
        self.data = a.get('https://angel.starkstate.edu/default.asp')
        self.emails = a.get('https://angel.starkstate.edu/Mail/MailHandler.ashx?apiaction=mail_headers&source=BLANK&folder=xxx&mask=mail.data.msgs%5B%7EMessageId%7E%5D%3Dnew%20Msg%28%7EMessageId%7E%2C%7EParentId%7E%2C%7EMsgDeleted%7E%2C%7E%23DateSent%23%7E%2C%7ESender%7E%2C%7ESenderName%7E%2C%7EAttachments%7E%2C%7ESubject%7E%2C%7EMsgPriority%7E%2C%7EDiscloseRecipients%7E%2C%7EFolderId%7E%2C%7ECourseId%7E%2C%7E%23date_Read%23%7E%2C%7EMsgDeleted%7E%2C%7EUserReadStatus%7E%2C%7ECurrentUserRights%7E%2C%7ERecipients%7E%2C%7ECcRecipients%7E%2C%7EBccRecipients%7E%2C%27%27%2Cfalse%29%3B%0A').text

    def courseList(self):
        x = self.data.text
        a = x.find('<strong>Courses</strong>')
        b = x.find('</ul><div style="text-align:right">')
        c = x[a+24:b-7]
        return c
    def allEmails(self): #Returns a list of all user's emails in form of a dictionary that contains dictionaries named after each emails id!
        xa = self.emails.split("\n")
        xb = len(xa)
        xb = xb - 2
        emails = {}
        while xb != -1:
            xc = xa[xb].split(',')
            mID = xc[0][16:52] #Message ID
            emails[mID] = {}
            emails[mID]['ParentId'] = xc[1]
            emails[mID]['MsgDeleted'] = xc[2]
            emails[mID]['DateSent'] = xc[3]
            emails[mID]['Sender'] = xc[4]
            emails[mID]['SenderName'] = xc[5] + "," + xc[6]
            emails[mID]['Attachments'] = xc[7]
            emails[mID]['Subject'] = xc[8]
            emails[mID]['MsgPriority'] = xc[9]
            emails[mID]['DiscloseRecipients'] = xc[10]
            emails[mID]['FolderId'] = xc[11]
            emails[mID]['CoruseId'] = xc[12]
            emails[mID]['date_Read'] = xc[13]
            emails[mID]['MsgDeleted'] = xc[14]
            emails[mID]['UserReadStatus'] = xc[15]
            emails[mID]['CurrentUserRights'] = xc[16]
            xb = xb - 1
        idlist = list(emails.keys())
        emails['idList'] = idlist
        return emails
        

s = Seraph("xxx", "xxx")
print s.courseList()
print "~~~Email Testing~~~"
aa = s.allEmails()
test = aa['xxx']['SenderName']
print test
print "~~~~~~~~~~~~~~~~"
print aa['idList'][0]
