from utils.tools import *
from utils.binTools import *
from datetime import datetime
import math

class solverKarg():
    def __init__(self):
        self.nameStudents = ["Ian Picado", "Jaron Cascante"]
        self.lastRunDate = datetime.now()
        self.numOfVariables = 0
        self.variables = []
        self.miniTerms = []
        self.dontCares = []
        self.miniTermsMerged = []
        self.primeImplicants = []
        self.essentialImplicants = []

    def run(self):
            exitProject = 0
            while exitProject == 0:
                numFiles = int(input("\nEnter the number of files:\n"))
                indexOfNumFiles = 0
                while indexOfNumFiles < numFiles:
                    try:
                        self.initialize()
                        self.processMiniterms()
                        self.resolveFn()

                        print("\nThe simplified function is:\n")

                        for term in self.essentialImplicants:
                            count=0
                            for i in range(len(term)):
                                if term[i]=='0':
                                    print(f""+self.variables[count]+"'",end="")
                                elif term[i] =="1":
                                    print(self.variables[count],end="")
                                count+=1
                            if len(self.essentialImplicants) -1 != self.essentialImplicants.index(term):
                                print(" + ",end="") 
                            else:
                                print("\n")

                        input("Press Enter to continue...\n")
                        clear()
                        indexOfNumFiles+=1

                        if indexOfNumFiles == numFiles:
                            flag = False
                            while flag == False:
                                res = str(input("\nYou want to run again the project? write 'Y' or 'N':\n"))
                                if res in ["Y", "y", "N", "n"]:
                                    flag = True
                            if res in ["N", 'n']:
                                exitProject = 1
                            else:
                                clear()

                    except Exception as e:
                        print(e)
                        res = ''
                        flag = False
                        while flag == False:
                            res = str(input("\nyou wanna try again? write 'Y' or 'N'\n"))
                            if res in ["Y", "y", "N", "n"]:
                                flag = True

                        if res in ["N", 'n']:
                            return 0
            
            

        
    def initialize(self):
        self.nameStudents = ["Ian Picado", "Jaron Cascante"]
        self.lastRunDate = datetime.now()
        self.numOfVariables = 0
        self.variables = []
        self.miniTerms = []
        self.dontCares = []
        self.miniTermsMerged = []
        self.primeImplicants = []
        self.essentialImplicants = []

        fileName = str(input("\nEnter the name of the file:\n"))
        if ".txt" not in fileName:
            fileName = fileName+".txt"
        clear()

        print(f"The specified file is: "+fileName)
        
        function = readTextFile(f"./"+fileName)

        function = function.split("f(")[1]

        thisVariables = function.split(")")[0]
        self.variables = [str(x.replace(" ", "")) for x in thisVariables.split(",")]
        self.numOfVariables = len(self.variables)

        minis = function.split("=")[1].split("/")[0] 
        self.miniTerms = [hexToBin(int(x), self.numOfVariables) for x in [int(x) for x in minis.split(",")]]

        if len(function.split("=")[1].split("/")) > 1:
            dcares = function.split("=")[1].split("/")[1] 
            self.dontCares = [hexToBin(int(x), self.numOfVariables) for x in [int(x) for x in dcares.split(",")]]

        self.miniTermsMerged = self.miniTerms + self.dontCares

    def processMiniterms(self):

        #primero se agrupan los miniterminos (con condiciones de no importa)
        #por el numero de 1 dentro de cada uno de los miniterminos

        group0,group1,group2,group3,group4,group5 = [], [], [], [], [], []

        try:
            for i in self.miniTermsMerged:
                if i.count("1") == 0:
                    group0.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                elif i.count("1") == 1:
                    group1.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                elif i.count("1") == 2:
                    group2.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                elif i.count("1") == 3:
                    group3.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                elif i.count("1") == 4:
                    group4.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                elif i.count("1") == 5:
                    group5.append({ 
                        'bin': i,
                        'hex': int(i,2)
                    })
                else:
                    raise Exception("more than 5 variables found!")
        except Exception as error:
            print(str(error))

        group6,group7,group8,group9,group10 = [], [], [], [], []

        group6 = firstCompare(group0, group1, group6, self.numOfVariables)
        group7 = firstCompare(group1, group2, group7, self.numOfVariables)
        group8 = firstCompare(group2, group3, group8, self.numOfVariables)
        group9 = firstCompare(group3, group4, group9, self.numOfVariables)
        group10 = firstCompare(group4, group5, group10, self.numOfVariables)

        group11,group12,group13,group14 = [], [], [], []
        
        group11 = secondCompare(group6, group7, group11, self.numOfVariables)
        group12 = secondCompare(group7, group8, group12, self.numOfVariables)
        group13 = secondCompare(group8, group9, group13, self.numOfVariables)
        group14 = secondCompare(group9, group10, group14, self.numOfVariables)
        
        group15,group16,group17 = [], [], []

        group15 = secondCompare(group11, group12, group15, self.numOfVariables)
        group16 = secondCompare(group12, group13, group16, self.numOfVariables)
        group17 = secondCompare(group13, group14, group17, self.numOfVariables)

        group18,group19 = [], []

        group18 = secondCompare(group15, group16, group18, self.numOfVariables)
        group19 = secondCompare(group16, group17, group19, self.numOfVariables)

        group20 = []

        group20 = thirdCompare(group18, group19, group20, self.numOfVariables)

        primeImplicants = group20
        flag = 0

        if len(primeImplicants) == 0:
            primeImplicants = group19 + group18
            flag = 1
        if len(primeImplicants) == 0:
            primeImplicants = group17 + group16 + group15
            flag = 2
        if len(primeImplicants) == 0:
            primeImplicants = group14 + group13 + group12 + group11
            flag = 3
        if len(primeImplicants) == 0:
            primeImplicants = group6 + group7 + group8 + group9 + group10
            flag = 4

        usedImplicants = []
        missingImplicants = []

        for f in primeImplicants:
            for y in f['hex']:
                usedImplicants.append(y)

        for y in self.miniTermsMerged:
            if binToHex(y) not in usedImplicants:
                missingImplicants.append(binToHex(y))
        
        if flag == 0:
            lastImplicantsGroup = group19 + group18
            primeImplicants = completePrimeImplicants(lastImplicantsGroup, missingImplicants, primeImplicants)

        elif flag == 1:
            lastImplicantsGroup = group17 + group16 + group15
            primeImplicants = completePrimeImplicants(lastImplicantsGroup, missingImplicants, primeImplicants)
            

        elif flag == 2:
            lastImplicantsGroup = group14 + group13 + group12 + group11
            primeImplicants = completePrimeImplicants(lastImplicantsGroup, missingImplicants, primeImplicants)
            

        elif flag == 3:
            lastImplicantsGroup = group6 + group7 + group8 + group9 + group10
            primeImplicants = completePrimeImplicants(lastImplicantsGroup, missingImplicants, primeImplicants)
        else:
            print("nothing here")

        self.primeImplicants = primeImplicants

    def resolveFn(self):
        essentialImplicants = []
        selectedImplicants = []        
        usedImplicants = []
        missingImplicants = []
        minimum=math.inf
        maximum = 0

        #se agrupan los implicantes primos por miniterminos en una tabla
        #con los miniterminos como columns y los implicantes como records
        
        for x in self.miniTerms:
            count = 0
            match = None
            for i in self.primeImplicants:
                print(i)
                for j in i["hex"]:
                    if binToHex(x) == j:
                        count += 1
                        match = i
            if count == 1:
                if match not in essentialImplicants:
                    essentialImplicants.append(match)

        for x in essentialImplicants:
            for i in x["hex"]:
                if i not in usedImplicants:
                    usedImplicants.append(i)

        for i in self.miniTermsMerged:
            if binToHex(i) not in usedImplicants:
                missingImplicants.append(binToHex(i))

        for i in self.primeImplicants:
            count = 0
            for j in i["hex"]:
                if j in missingImplicants:
                        count += 1
                if count > maximum:
                    maximum = count
        
        for implicant in self.primeImplicants:
            count = 0
            for j in implicant["hex"]:
                if j in missingImplicants:
                        count += 1
                if count == maximum:
                    if implicant not in selectedImplicants:
                        selectedImplicants.append(i)
        
        #tomamos el implicante con menos unos para optimizar memoria
        for implicant in selectedImplicants:
            count = 0
            for i in range(len(implicant["bin"])):
                if implicant["bin"][i] =='0' or implicant["bin"][i]=='1':
                    count+=1
            if count<minimum:
                minimum=count

        for implicant in selectedImplicants:
            count = 0
            for i in range(len(implicant["bin"])):
                if implicant["bin"][i] =='0' or implicant["bin"][i]=='1':
                    count+=1
            if count==minimum:
                if implicant not in essentialImplicants:
                    essentialImplicants.append(implicant)

        print(essentialImplicants)
        self.essentialImplicants = [x["bin"] for x in essentialImplicants]
   