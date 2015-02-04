class boa(object):
    def __init__(self, string):#Assuming that this markup language is like xml or html
        #self.f = []#First occurences of tag
        #self.l = []#Last occurences of tag
        #Plan To Include Another Module Version With MultiThreading
        self.data = string                       #Object storage of the string

    def parameterAnalysis(self,x,y,z):           #To deal with opening tags containing parameters
        d = {}
        if x != 'none':
            a = x.split(' ')
            b = len(a) - 1
            if b==' ':                           #This if is just incase that a tag being analyzed is like <span id="waht" > instead of <span id="what"> *the empty unecessary space in end
                del a[-1]
            while b != -1:
                c = a[b].split('=')
                c[1] = c[1].strip("'")
                c[1] = c[1].strip('"')
                d[c[0]]=c[1]
                b = b - 1
            e = list(d.keys())
            d['parameters'] = e
        else:
            d['parameters'] = 'none'
        d['content'] = z
        self.instances.append(d)                #Possible just return d when called, so parameterAnalysis doesn't need to include self. Does not including slef make it faster?

    def readMarkups(self,ot,otl,otp,ct,oto,cto):
        self.instances = []      #Array of dictionaries, where each dictionary is the data collected from each instance of tag
        if oto != cto:           #If there are an uneven distribution of opening and closing tags
            print "There are an uneven number of opening and closing tags in this string!"
            print oto
            print cto
        else:
            fci = 0
            z = self.data
            while fci != oto:
                h = len(z)
                a = z.find(ot)
                b = z.find(otp)
                #The if-statement determines whether or not the the plain tag or tag with parameters is first
                if a>b and b != -1:
                    v = z[b+otl:h]
                    l = v.find('>')
                    v = v[0:l]                #Tag Parameters In $$$="%%%" Format, Spererated By Spaces
                    f = len(v) + otl + 2
                    q = b
                else:
                    q = a
                    v = 'none'
                    f = otl + 1
                c = z.find(ct)
                r = z[q+f-1:c]                #Contains the content between the tags
                z = z[c+otl+1:h]              #Shortens string by removing the closing tag analyzed and all data before it!
                self.parameterAnalysis(v,0,r) #Sends all the different Parameter Tags and There Values To Be Indexed   ~ 1 being a temporary input, 1 will be replaced for an instance beign counted.
                fci = fci + 1

    def scrapeByTag(self, tag):
        ot = tag                            #Opening Tag
        otl = len(tag)                      #Length of Opening Tag
        otp = tag[0:otl-1] + ' '            #Incase the opening tag has parameters
        ct = tag[0] + '/' + tag[1:otl]      #Closign Tag
        string = self.data
        x = string.count(ot)
        y = string.count(otp)
        if x == -1:
            x = 0
        elif y == -1:
            y = 0
        oto = x + y                         #How many times the opening tag appears
        cto = string.count(ct)              #How many times the closing tag appears
        self.readMarkups(ot, otl, otp, ct, oto, cto)
    #uid:'663554', username:'d4768a91-e3e7-4fd7-be27-7f89687068d7',
    def renderDictionary(self, l):
        a = l.split(',')
        b = len(a) - 1
        rD = {}
        while b != -1:
            c = a[b].split(":'")
            d = c[0].strip()
            e = c[1].replace("'", "")
            rD[d] = e
            b = b - 1
        return rD
    #Need A Function that converts unicode utf-8 to ASCII
    
                



