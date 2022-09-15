from utils.textFiles import *
from utils.binUtils import *
from datetime import datetime

class solverKarg():
    def __init__(self):
        self.nameStudents = ["Ian Picado", "Jaron Cascante"]
        self.lastRunDate = datetime.now()
        self.numOfVariables = 0
        self.variables = []
        self.miniTerms = []

        self.miniTermsCategorised = {}
        self.primeImplicants = []

    def run(self):
            numFiles = int(input("Enter the number of files:\n"))
            indexOfNumFiles = 0
            while indexOfNumFiles < numFiles:
                try:
                    self.initialize()
                    self.processMiniterms()
                    # self.getPrimeImplicants(self.miniTermsCategorised, self.numOfVariables)

                    # essential_implicants, functions = self.resolveFn()
                    # print(functions)
                    # print("\nThe prime implicants are:")
                    # self.printing([x[0] for x in self.primeImplicants],',')

                    # print("\nThe essential implicants are:")
                    # self.printing(essential_implicants,',')

                    # print("\nThe possible functions are:")
                    # for i in functions :
                    #     self.printing(i,'+')
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
    
    def printing(self,mainList,char):
        for char in mainList:
            count=-1
            for i in range(len(str(char))):
                count+=1
                if str(char[i])=='0':
                    print(self.variables[count]+"'",end="")
                elif str(char[i]) =="1":
                    print(self.variables[count],end="")
            print("  "+"+"+"  ",end="")
        print("\b\b\b \n")
        
    def initialize(self):
        self.nameStudents = ["Ian Picado", "Jaron Cascante"]
        self.lastRunDate = datetime.now()
        self.numOfVariables = 0
        self.miniTerms = []
        self.miniTermsCategorised = {}
        self.primeImplicants = []

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

        self.dontCare = [int(x) for x in function.split("/")[1] if x.isdigit() == True] if "/" in function else []
        self.miniTerms = [hexToBin(int(x), self.numOfVariables) for x in function if x.isdigit() == True]
        
        for i in range(self.numOfVariables + 1):
            self.miniTermsCategorised[i] = None

        for i in self.miniTerms:
            self.miniTermsCategorised[i.count("1")] = i
    
    def getPrimeImplicants(self, terms: dict = {}, number = 0):
        
        newTerms={}
        usedTerms=[]
        isRecursive=False

        for i in range(number):
            newTerms[i]=[]

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
                            
                    if count <= 1:
                        isRecursive=True
                        flag=1
                        new_implicant = ["".join(combined),element1[1]+element2[1]] 
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

    def condition1(self,  k, i):
        return self.miniTermsCategorised[k][i] != self.miniTermsCategorised[k + 1][i] \
            if self.miniTermsCategorised[k + 1] != None else False
    
    def condition2(self, a, k, i):
        if(k == len(a) - 1):
            return False
        return a[k][i] != a[k + 1][i]
           
    def processMiniterms(self):
        a, b = [], []

        for k in self.miniTermsCategorised:
            count = 0
            combined = []
            for i in range(self.numOfVariables):
                if self.miniTermsCategorised[k] is not None:
                    combined.append(self.miniTermsCategorised[k][i])
                    if(self.condition1(k, i)):
                        combined[i] = "-"
                        count += 1
            if(count == 1):
                a.append(combined)
        print(a)

        for k in range(len(a)):
            count = 0
            combined = []
            for i in range(len(a[k])):
                combined.append(a[k][i])
                if(self.condition2(a, k, i)):
                    combined[i] = "-"
                    count += 1
            if(count == 1):
                b.append(combined)

        print(b)


        # def step2(b):
        #     for k in range(len(b)):
        #         count = 0
        #         combined = []
        #         for i in range(len(self.numOfVariables)):
        #             combined.append(b)
        #             if(condition(k, i)):
        #                 combined[i] = "-"
        #                 count += 1
        #         if(count == 1):
        #             a.append(combined)





    def count(self,mainList):
        count =0
        for char in mainList:
            for i in range(len(mainList[1])):
                if char[i] =='0' or char[i]=='1':
                    count+=1

        return count

    def resolveFn(self):
        minimum=999999
        table={}
        essential_implicants = []
        selected_implicants = []
        missing_implicants = []
        minimal_implicants = []
        functions = []

        for i,j in self.miniTermsCategorised.items():
            for k in j:
                table[k[1][0]]=[]
                    
        for i in self.primeImplicants:
            for j in i[1]:
                table[j].append(i)

        for i in [x for x in table if len(table[x])==1]:
            if table[i][0] not in essential_implicants:
                essential_implicants.append(table[i][0])
        
        used_implicants = []

        for x in essential_implicants:
            for i in x[1]:
                if i not in used_implicants:
                    used_implicants.append(i)

        
        for i in self.miniTerms:
            term = int(i,2)
            if term not in used_implicants:
                missing_implicants.append(term)
        
        maximum = 0

        for i in table:
            for w in table[i]:
                count = 0
                for j in w[1]:
                    if j in missing_implicants:
                        count +=1
                if count > maximum:
                    maximum = count

        for i in table:
            for w in table[i]:
                count = 0
                for j in w[1]:
                    if j in missing_implicants:
                        count +=1
                if count == maximum:
                    if w not in selected_implicants:
                        selected_implicants.append(w)

        for i in selected_implicants:
            if self.count(i)<minimum:
                minimum=self.count(i)

        for i in selected_implicants:
            if self.count(i)==minimum:
                minimal_implicants.append(i)
        
        for i in minimal_implicants:
            functions.append( essential_implicants+i )
        print(functions)

        essential_implicants = [x[0] for x in essential_implicants]

        for char in mainList:
            for i in range(len(functions)):
                functions[i] = []

        for i in range (len(functions)):
            functions[i] = [x[0] for x in functions[i]]
 
        return essential_implicants, functions
   