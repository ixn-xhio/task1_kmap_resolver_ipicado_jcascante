from utils.textFiles import *
from datetime import datetime

class solverKarg():
    def __init__(self):
        self.nameStudents = ["Ian Picado", "Jaron Cascante"]
        self.lastRunDate = datetime.now()
        self.numOfVariables = 0
        self.miniTerms = []
        self.miniTermsCategorised = {}
        self.primeImplicants = []

    def run(self):
            numFiles = int(input("Enter the number of files:\n"))
            indexOfNumFiles = 0
            while indexOfNumFiles < numFiles:
                try:
                    self.initialize()
                    prime_implicants, essential_implicants, functions = self.quineMcCluskey()
                    
                    print("\nThe prime implicants are:")
                    self.printing(prime_implicants,',')

                    print("\nThe essential implicants are:")
                    self.printing(essential_implicants,',')

                    print("\nThe possible functions are:")
                    for i in functions :
                        self.printing(i,'+')
                    indexOfNumFiles+=1

                except Exception as e:
                    print(e)
                    res = ''
                    flag = False
                    while flag == False:
                        res = str(input("you wanna try again? write 'Y' or 'N'\n"))
                        if res in ["Y", "y", "N", "n"]:
                            flag = True

                    if res in ["N", 'n']:
                        return 0

    def initialize(self):
        fileName = str(input("Enter the name of the file:\n"))
        function = ""
        
        if ".txt" in fileName:
            function = readTextFile(f"./"+fileName)
        else:
            function = readTextFile(f"./"+fileName+".txt")

        function = function.split("f(")[1]

        thisVariables = function.split(")")[0]
        self.variables = [str(x.replace(" ", "")) for x in thisVariables.split(",")]
        self.numOfVariables = len(self.variables)

        thisMiniterms = function.split("=")[1].split("/")[0]
        thisMiniterms = [int(x) for x in thisMiniterms.split(",")]
        self.miniTerms = [format(int(x), f'0'+str(self.numOfVariables)+'b') for x in thisMiniterms]

        for i in range (self.numOfVariables+1):
            self.miniTermsCategorised[i]=[]
        for i in self.miniTerms:
            self.miniTermsCategorised[i.count("1")].append([i,[int(i,2)]])

    def printing(self,mainList,char):
        for string in mainList:
            count=-1
            for i in string:
                count+=1
                if i=='0':
                    print(chr(ord('a')+count)+"'",end="")
                elif i =="1":
                    print(chr(ord('a')+count),end="")
            print(" "+char+" ",end="")
        print("\b\b\b \n")
    
    def getPrimeImplicants(self, terms: dict = {}, number = 0):
        newTerms={}
        usedTerms=[]
        isRecursive=False
        for i in range(number):
            newTerms[i]=[]
        for i in range(number):
            for element1 in terms[i]:
                flag=0
                for element2 in terms[i+1]:
                    count=0
                    combined=[]
                    for l in range(len(element1[0])):
                        combined.append(element1[0][l])
                        if element2[0][l]!=element1[0][l]:
                            combined[l]='-'
                            count+=1
                    if not count > 1:
                        new_implicant = ["".join(combined),element1[1]+element2[1]] 
                        isRecursive=True
                        flag=1
                        newTerms[i].append(new_implicant)
                        if element1[0] not in usedTerms:
                            usedTerms.append(element1[0])
                        if element2[0] not in usedTerms:
                            usedTerms.append(element2[0])

                if flag==0:
                    if element1[0] not in usedTerms and element1[0] not in [x[0] for x in self.primeImplicants]:
                        self.primeImplicants.append(element1)

        if isRecursive:
            self.getPrimeImplicants(newTerms,number-1)
        else:
            return

    def getAllSelected(self,POS,temp,allSelected,index):
        if index==len(POS):
            temp1=temp+[]
            allSelected.append(temp1)
            return
        else:
            for i in POS[index]:
                if i not in temp:
                    temp.append(i)
                    self.getAllSelected(POS,temp,allSelected,index+1)
                    temp.remove(i)
                else:
                    self.getAllSelected(POS,temp,allSelected,index+1)

    def petrickMethod(self,table,selected_implicants):
        temp=[]
        POS=[]
        allSelected=[]
        for i in table:
            POS.append(table[i])
        self.getAllSelected(POS,temp,allSelected,0)

        for i in allSelected:
            if len(i)==min([len(x) for x in allSelected]):
                if i not in selected_implicants:
                    selected_implicants.append(i)

    def getcount(self,mainList):
        count =0
        for string in [x[0] for x in mainList]:
            for i in string:
                if i=='0' or i=='1':
                    count+=1

        return count

    def quineMcCluskey(self):
        table={}
        essential_implicants = []
        selected_implicants = []
        minimal_implicants = []
        functions = []

        self.getPrimeImplicants(self.miniTermsCategorised, self.numOfVariables)
        print(self.miniTermsCategorised)
        for i,j in self.miniTermsCategorised.items():
            for k in j:
                print(k)
                table[k[1][0]]=[]

        for j in self.miniTermsCategorised:
                for k in self.miniTermsCategorised[i]:
                    print(k)
        for i in self.primeImplicants:
            for j in i[1]:
                table[j].append(i)

        for i in [x for x in table if len(table[x])==1]:
            if table[i][0] not in essential_implicants:
                essential_implicants.append(table[i][0])
            del table[i]

        for i in essential_implicants:
            for j in i[1]:
                if j in [x for x in table]:
                    del table[j]

        self.petrickMethod(table,selected_implicants)

        minimum=999999
        for i in selected_implicants:
            if self.getcount(i)<minimum:
                minimum=self.getcount(i)

        for i in selected_implicants:
            if self.getcount(i)==minimum:
                minimal_implicants.append(i)
        
        for i in minimal_implicants:
            functions.append( essential_implicants+i )

        prime_implicants = [x[0] for x in self.primeImplicants]
        essential_implicants = [x[0] for x in essential_implicants]

        for i in range (len(functions)):
            functions[i] = [x[0] for x in functions[i]]

        return prime_implicants, essential_implicants, functions


                    