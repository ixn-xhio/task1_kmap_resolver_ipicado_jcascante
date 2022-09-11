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
                    self.getPrimeImplicants(self.miniTermsCategorised, self.numOfVariables)
                    print(self.primeImplicants)
                    print(self.miniTermsCategorised)
                    print(self.miniTerms)
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

        varis = function.split(")")[0]
        self.variables = [str(x.replace(" ", "")) for x in varis.split(",")]
        
        minis = function.split("=")[1].split("/")[0]
        minis = [int(x) for x in minis.split(",")]
        self.numOfVariables = len(variables)
        self.miniTerms = [format(int(x), f'0'+str(self.numOfVariables)+'b') for x in minis]

        for i in range (self.numOfVariables+1):
            self.miniTermsCategorised[i]=[]
        for i in self.miniTerms:
            self.miniTermsCategorised[i.count("1")].append([i,[int(i,2)]])


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


                    