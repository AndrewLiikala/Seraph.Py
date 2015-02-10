import requests
from Boa import boa
class Seraph(object):

    def __init__(self, username, password):
        self.a = requests.session()
        b = dict(username=username,password=password)
        self.eID = self.a.post('https://angel.starkstate.edu/signon/authenticate.asp', data=b) #self.eId is the error code recieved
        self.data = self.a.get('https://angel.starkstate.edu/default.asp')

    def courseList(self):
        a = boa(self.data.text)
        b = a.getTagLocations('<ul>')
        c = a.getTagProperties(b)
        d = len(c) - 1
        e = []
        while d != -1: #Starts search at bottom of array, shoudln't make much of a difference
            if 'class' in c[d]['parameters']:
                if c[d]['class'] == 'mktree':
                    e.append(c[d])
            d = d - 1
        if len(e)==0: #Error Checking-ish
            print 'No Parameters Were Found'
        elif len(e)>1:
            print 'Multiple tags share the same parameter value!'
        f = e[0]['content']
        a = boa(f)
        b = a.getTagLocations('<a>')
        c = a.getTagProperties(b)
        d = a.getTagLocations('<span>')
        e = a.getTagProperties(d)
        f = 0
        g = {}
        while f!=5:
            g[e[f]['content']] = c[f]['href']
            f = f + 1
        return g

    def userData(self):
        x = self.data.text
        a = x.find('ANGEL.user') + 14
        b = x.find('ANGEL.section') - 4
        c = x[a:b]
        d = boa(c).renderDictionary(c)
        return d

    def emailFolders(self):
        y = self.a.get('https://angel.starkstate.edu/Mail/MailHandler.ashx?apiaction=mail_folders&source=BLANK&mask=mail.data.folders%5B%7EFolderId%7E.toUpperCase%28%29%5D%3D%7B%27folderId%27%3A%7EFolderId%7E.toUpperCase%28%29%2C%27folderName%27%3A%7EFolderName%7E%2C%27systemFolder%27%3A%7ESystemFolder%7E%2C%27unreadCount%27%3A%7EUnreadMessageCount%7E%2C%27messageCount%27%3A%7EMessageCount%7E%7D%3B%0A').text
        a = y.split('\n')
        b = len(a)
        b = b - 2
        folders = {}
        while b != -1:
            c = a[b].split(",")
            d = c[0].find('.toUpperCase()')
            e = c[0][19:d - 1].upper()
            f = c[1].split(':')
            g = c[2].split(':')
            h = c[3].split(':')
            i = c[4].split(':')
            j = len(i) + 1
            k = i[1][:j]
            folders[e] = {}
            folders[e]['folderName'] = f[1]
            folders[e]['systemFolder'] = g[1]
            folders[e]['unreadCount'] = h[1]
            folders[e]['messageCount'] = k
            b = b - 1
        tt = list(folders.keys())
        folders['idList'] = tt
        return folders

    def getEmails(self, fid): #Returns a list of all user's emails from folder with id of variable fid, in form of a dictionary that contains dictionaries named after each emails id!
        xex = self.a.get('https://angel.starkstate.edu/Mail/MailHandler.ashx?apiaction=mail_headers&source=BLANK&folder=' + str(fid) + '&mask=mail.data.msgs%5B%7EMessageId%7E%5D%3Dnew%20Msg%28%7EMessageId%7E%2C%7EParentId%7E%2C%7EMsgDeleted%7E%2C%7E%23DateSent%23%7E%2C%7ESender%7E%2C%7ESenderName%7E%2C%7EAttachments%7E%2C%7ESubject%7E%2C%7EMsgPriority%7E%2C%7EDiscloseRecipients%7E%2C%7EFolderId%7E%2C%7ECourseId%7E%2C%7E%23date_Read%23%7E%2C%7EMsgDeleted%7E%2C%7EUserReadStatus%7E%2C%7ECurrentUserRights%7E%2C%7ERecipients%7E%2C%7ECcRecipients%7E%2C%7EBccRecipients%7E%2C%27%27%2Cfalse%29%3B%0A').text
        xa = xex.split("\n") #Have to convert to string here, because the function getEmails will usually take in variable   ^^^^^   fid as a list object, due to dictionary returned by emailFolders
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

    def testAction(self, x):
        pd = self.a.get(x).text
        print pd

    def close(self):  #Closes the Requests Session
        self.a.close()

s = Seraph("aliikala0518", "apl.279021")
y = s.courseList()
print y
s.close()



