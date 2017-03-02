# file boulder.py

class Area(object):

    def __init__ (self, name):
        self.name = name
        self.info = None
        self.boulder_list = []
        self.topo_list = []

    def getName(self):
        return self.name

    def setInfo(self,info):
        self.info = info

    def getInfo(self):
        return self.info

    def addBoulder(self,boulder):
        self.boulder_list.append(boulder)

    def getBoulderlist(self):
        for boul in self.boulder_list:
            print boul.getName()

    def getBouldernumber(self):
        return len(self.boulder_list)

    def addTopo(self,topo):
        self.topo_list.append(topo)

    def getTopolist(self):
        return self.topo_list

    def getToponumber(self):
        return len(self.topo_list)

class Boulder(dict):

    def __init__(self):
        self.name = "n/a"
        self.numb = None
        self.info = None
        self.ascents = None
        self.grade = []
        self.opener = []
        self.style = []

    def __setitem__(self, key, item): 
        self.__dict__[key] = item
    
    def __getitem__(self, key): 
        return self.__dict__[key]

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name

    def setGrade(self,value):
        self.grade.append(value)

    def getGrade(self):
        return self.grade

    def setOpener(self,value):
        self.opener.append(value)

    def getOpener(self):
        return self.opener

    def setStyle(self,value):
        self.style.append(value)

    def getStyle(self):
        return self.style

    def setInfo(self,info):
        self.info = info

    def getInfo(self):
        return self.info
    
    def setNumb(self,numb):
        self.numb = numb

    def getNumb(self):
        return self.numb

    def setAscents(self,ascents):
        self.ascents = ascents

    def getAscents(self):
        return self.ascents

