#file patients.py
class User():
    def __init__(self, id, password):
        try:
            self.id = int(id)
        except:
            self.id = None   
        self.password = password
    
    
class Patient(User):
    _registery = []
    def __init__(self,id, password, salution, fName, mName="", lName=""):
        User.__init__(self, id, password)
        self._registery.append(self)
        self.salution=salution
        self.__mName = mName
        self.__fName=fName
        self.__lName=lName
        self.__rev = 0
    def getfName(self):
        return self.__fName
    def getlName(self):
        return self.__lName
    def getRev(self):
        return self.__rev
    def setfName(self,name):
        self.__fName = name
    def setlName(self, name):
        self.__lName = name
    def addRev(self,num):

        try: 
            self.__rev += float(num)
        except: 
            return('Invalid')
    def getmName(self):
        return self.__mName
    def setmName(self,name):
            self.__mName = name
    def display(self):
        print("Patient name:", self.salution, self.__fName, self.__mName, self.__lName)
        print("Revenue: ", self.__rev)
        return(0)

