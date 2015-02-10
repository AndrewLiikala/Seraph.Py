class boa(object):
    def __init__(self, string):#Assuming that this markup language is like xml or html
        #self.f = []#First occurences of tag
        #self.l = []#Last occurences of tag
        #Plan To Include Another Module Version With MultiThreading
        self.data = string                       #Object storage of the string

    def getTagLocations(self,tag):          #Function returns a list that contains all of the locations of the called tag, each index of returned array is a grouping of an opening tag and it's closing tag
        ot = tag                            #Opening Tag
        otl = len(tag)                      #Length of Opening Tag
        otp = tag[0:otl-1] + ' '            #Incase the opening tag has parameters
        ct = tag[0] + '/' + tag[1:otl]      #Closign Tag
        x = self.data
        z = x
        #
        oti = []                            #Array for containing each instance of opening tag in document
        cti = []                            #Array for containing each instance of closing tag in document
        atl = []                            #Master array for containg instances of tag locations in order as they appear
        stpr = 0                            #Variable for stoping below loop when it finds every tag
        search = []                         #Array containing the tag variations to look for in the following order...
        search.append(ot)                   #Opening tags without parameters
        search.append(otp)                  #Opening tags with parameters
        search.append(ct)                   #Closing tags with parameters
        si = 0
        while si != 3:                      #Algorithm that finds the locations of all of the opening and closing tags in the order mentioned above
            z = x
            gv = 0
            stpr = 0
            while stpr != 1:
                a = z.find(search[si])
                if a==-1:
                    stpr = 1
                if si==2:
                    q = otl + 1
                elif si==0:
                    q = otl
                else:
                    qq = z[a:]
                    q = qq.find('>') + 1
                z = z[a+q:]
                coords = []
                coords.append(a + gv)
                coords.append(a+gv+q)
                if si == 2:
                    cti.append(coords)
                else:
                    oti.append(coords)
                gv = gv + a + q
            if si==0 or si==1:              #Note to self, if something bugged with outputted cti or oti, check here!
                del oti[-1]
            else:
                del cti[-1]
            si = si + 1
        #Now oti is an array that contains smaller arrays, the first index of the smaller array is the index where the tag begins, and the second index is where the tag ends
        #Now cti is an array that contains smaller arrays, the first index of the smaller array is the index where the tag begins, and the second index is where the tag ends
        a = len(oti)
        b = len(cti)
        aa = 0
        bb = 0
        while aa<a and bb<b:
            if oti[aa][1]<cti[bb][0]:
                atl.append(oti[aa])
                aa=aa+1
            else:
                atl.append(cti[bb])
                bb=bb+1
        if aa==a: #If oti is at end
            while bb<b:
                atl.append(cti[bb])
                bb = bb + 1
        else:
            while aa<a:
                atl.append(oti[aa])
                aa = aa + 1
        #Now we also have atl, which is a combined list of oti and cti; in numberical order of course
        sa = [] #array used for stacking algorithm
        gt = [] #Array that houses the master list for grouped tags
        a = len(atl)
        b = 0
        c = 0
        d = 0
        while b!=a: #This algorithm deterimes which tags are grouped together. Decided to have a seperate function later on determine what is nested or not, for dealing with cross-tag nesting in a document
            c = len(sa) - 1
            if atl[b] in oti:
                sa.append(atl[b])
            elif atl[b] in cti and c!=-1:
                tg = []
                tg.append(sa[-1])
                tg.append(atl[b])
                gt.append(tg)
                del sa[-1]
            b=b+1
        return gt  #Format of returned array looks like this [[[],[]],[[],[]]]

    def getAllTags(self):
        x = self.data
        c = x.count('<') + 1
        cc = c
        d = x.count('>') + 1
        e = 0
        g = []
        b = x
        while e!=cc:
            a = b.find('<')
            b = b[a:]
            c = b.find(' ')
            d = b.find('>')
            if d>c:
                f = b[0:c] + '>'
            else:
                f = b[0:d + 1]
            if '/' not in f and f!='':
                if not f in g:
                    g.append(f)
            h = len(f)
            b = b[h:]
            e = e + 1
        return g

    def getAllTagLocations(self):  # Returns a dictionary that has a key for each type of tag found in the document, then each dictionary key returns
        a = self.getAllTags()      # an array containing a list of grouped tags and their locations.
        b = len(a)
        c = 0
        f = {}
        while c!=b:
            d = self.getTagLocations(a[c])
            f[a[c]]=d
            c = c + 1
        return f

    def getTagContent(self,x):     # When sent an array containing grouped tags, it sends back an array(in same order) containing the content between the tags.
        a = x
        b = self.data
        c = len(x)
        d = 0
        f = []
        while d!=c:
            h = a[d][0][1]
            g = a[d][1][0]
            e = b[h:g]
            f.append(e)
            d = d + 1
        return f

    def getTagProperties(self, x): # Returns an array containing a dictionary for each set of grouped coords(in same order), where each dictionary contains a list of parameters,
        a = x                      # parameter values with keys named after paramter type and content between tags.
        b = self.data
        m = self.getTagContent(a)
        c = len(a)
        d = 0
        f = []
        while d!=c:
            h = a[d][0][0]
            g = a[d][0][1]
            e = b[h+1:g-1]
            z = {}
            if ' ' not in e:
                z['parameters'] = ('none')
            else:
                g = e.split(' ')
                h = len(g)
                i = 1
                while i!=h:
                    if g[i]!='':
                        if '="' in g[i]:
                            j = g[i].split('="')
                        else:
                            j = g[i].split("='")
                        k = j[1].replace('"', '')
                        k = k.replace("'", '')
                        z[j[0]] = k
                    i = i + 1
                l = list(z.keys())
                z['parameters'] = l
            z['content'] = m[d]
            f.append(z)
            d = d + 1
        return f

