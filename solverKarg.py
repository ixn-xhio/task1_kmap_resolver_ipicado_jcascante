from utils.textFiles import *
from utils.binUtils import *
from datetime import datetime
import sys
import math

class solverKarg():
    def __init__(self):
        print(sys.version)
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
                    self.resolveFn()
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
        self.variables = []
        self.miniTerms = []
        self.dontCares = []
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

        minis = function.split("=")[1].split("/")[0] 
        self.miniTerms = [hexToBin(int(x), self.numOfVariables) for x in [int(x) for x in minis.split(",")]]

        if len(function.split("=")[1].split("/")) > 1:
            dcares = function.split("=")[1].split("/")[1] 
            self.dontCares = [int(x) for x in [int(x) for x in dcares.split(",")]]


    def processMiniterms(self):
        group0,group1,group2,group3,group4,group5 = [], [], [], [], [], []

        try:
            for i in self.miniTerms:
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
            print(repr(error))
        
        group6,group7,group8,group9,group10 = [], [], [], [], []

        for i in range(len(group0)):
            for j in range(len(group1)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group0[i]["bin"][k]
                    if group0[i]['bin'][k] != group1[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group6]:
                        group6.append({
                            'bin': combined,
                            'hex': [group0[i]['hex'], group1[j]['hex']]
                        })
        
        for i in range(len(group1)):
            for j in range(len(group2)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group1[i]["bin"][k]
                    if group1[i]['bin'][k] != group2[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group7]:
                        group7.append({
                            'bin': combined,
                            'hex': [group1[i]['hex'], group2[j]['hex']]
                        })

        for i in range(len(group2)):
            for j in range(len(group3)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group2[i]["bin"][k]
                    if group2[i]['bin'][k] != group3[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group8]:
                        group8.append({
                            'bin': combined,
                            'hex': [group2[i]['hex'], group3[j]['hex']]
                        })
        
        for i in range(len(group3)):
            for j in range(len(group4)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group3[i]["bin"][k]
                    if group3[i]['bin'][k] != group4[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group9]:
                        group9.append({
                            'bin': combined,
                            'hex': [group3[i]['hex'], group4[j]['hex']]
                        })

        for i in range(len(group4)):
            for j in range(len(group5)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group4[i]["bin"][k]
                    if group4[i]['bin'][k] != group5[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group10]:
                        group10.append({
                            'bin': combined,
                            'hex': [group4[i]['hex'], group5[j]['hex']]
                        })

        group11,group12,group13,group14 = [], [], [], []

        for i in range(len(group6)):
            for j in range(len(group7)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group6[i]["bin"][k]
                    if group6[i]['bin'][k] != group7[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group11]:
                        group11.append({
                            'bin': combined,
                            'hex': group6[i]['hex'] + group7[j]['hex']
                        })
        
        for i in range(len(group7)):
            for j in range(len(group8)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group7[i]["bin"][k]
                    if group7[i]['bin'][k] != group8[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group12]:
                        group12.append({
                            'bin': combined,
                            'hex': group7[i]['hex'] + group8[j]['hex']
                        })
        
        for i in range(len(group8)):
            for j in range(len(group9)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group8[i]["bin"][k]
                    if group8[i]['bin'][k] != group9[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group13]:
                        group13.append({
                            'bin': combined,
                            'hex': group8[i]['hex'] + group9[j]['hex']
                        })
        
        for i in range(len(group9)):
            for j in range(len(group10)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group9[i]["bin"][k]
                    if group9[i]['bin'][k] != group10[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group14]:
                        group14.append({
                            'bin': combined,
                            'hex': group9[i]['hex'] + group10[j]['hex']
                        })
        
        group15,group16,group17 = [], [], []

        for i in range(len(group11)):
            for j in range(len(group12)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group11[i]["bin"][k]
                    if group11[i]['bin'][k] != group12[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group15]:
                        group15.append({
                            'bin': combined,
                            'hex': group11[i]['hex'] + group12[j]['hex']
                        })

        for i in range(len(group12)):
            for j in range(len(group13)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group12[i]["bin"][k]
                    if group12[i]['bin'][k] != group13[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group16]:
                        group16.append({
                            'bin': combined,
                            'hex': group12[i]['hex'] + group13[j]['hex']
                        })

        for i in range(len(group13)):
            for j in range(len(group14)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group13[i]["bin"][k]
                    if group13[i]['bin'][k] != group14[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group17]:
                        group17.append({
                            'bin': combined,
                            'hex': group13[i]['hex'] + group14[j]['hex']
                        })

        print(group15,group16,group17)

        group18,group19 = [], []

        for i in range(len(group15)):
            for j in range(len(group16)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group15[i]["bin"][k]
                    if group15[i]['bin'][k] != group16[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group18]:
                        group18.append({
                            'bin': combined,
                            'hex': group15[i]['hex'] + group16[j]['hex']
                        })

        for i in range(len(group16)):
            for j in range(len(group17)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group16[i]["bin"][k]
                    if group16[i]['bin'][k] != group17[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group19]:
                        group19.append({
                            'bin': combined,
                            'hex': group16[i]['hex'] + group17[j]['hex']
                        })
        
        print(group18,group19)
        
        group20 = []

        for i in range(len(group18)):
            for j in range(len(group19)):
                count = 0
                combined = ""
                for k in range(self.numOfVariables):
                    combined += group18[i]["bin"][k]
                    if group18[i]['bin'][k] == '-' and group19[j]['bin'][k] == '-':
                        count += 1
                        combined = combined[:k] + "-"
                if count == 2:
                    if combined not in [x["bin"] for x in group20]:
                        group20.append({
                            'bin': combined,
                            'hex': group18[i]['hex'] + group19[j]['hex']
                        })
        
        z = group20
        flag = 0
        if len(z) == 0:
            z= group19 + group18
            flag = 1
        if len(z) == 0:
            z= group17 + group16 + group15
            flag = 2
        if len(z) == 0:
            z= group14 + group13 + group12 + group11
            flag = 3
        if len(z) == 0:
            z= group6 + group7 + group8 + group9 + group10
            flag = 4

        zTerms = []
        zMissing = []

        for f in z:
            for y in f['hex']:
                zTerms.append(y)

        for y in self.miniTerms:
            if binToHex(y) not in zTerms:
                zMissing.append(binToHex(y))
        
        if flag == 0:
            pivot = group19 + group18
            for implicant in pivot:
                count = 0
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                if count == 0:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        zMissing = []

            for implicant in pivot:
                count = 0
                match = None
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                    else:
                        match = missing
                if count == 1:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        del zMissing[zMissing.index(match)]

        if flag == 1:
            pivot = group17 + group16 + group15
            for implicant in pivot:
                count = 0
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                if count == 0:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        zMissing = []

            for implicant in pivot:
                count = 0
                match = None
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                    else:
                        match = missing
                if count == 1:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        del zMissing[zMissing.index(match)]

        if flag == 2:
            pivot = group14 + group13 + group12 + group11
            for implicant in pivot:
                count = 0
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                if count == 0:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        zMissing = []

            for implicant in pivot:
                count = 0
                match = None
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                    else:
                        match = missing
                if count == 1:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        del zMissing[zMissing.index(match)]

        if flag == 3:
            pivot = group6 + group7 + group8 + group9 + group10
            for implicant in pivot:
                count = 0
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                if count == 0:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        zMissing = []

            for implicant in pivot:
                count = 0
                match = None
                for missing in zMissing:
                    if missing not in implicant["hex"]:
                        count += 1
                    else:
                        match = missing
                if count == 1:
                    if(implicant["bin"] not in [x["bin"] for x in z]):
                        z.append(implicant)
                        del zMissing[zMissing.index(match)]
            
        self.primeImplicants = z

    def count(self,mainList):
        count =0
        for char in mainList:
            for i in range(len(mainList[1])):
                if char[i] =='0' or char[i]=='1':
                    count+=1

        return count

    def resolveFn(self):
        minimum=math.inf
        table={}
        essential_implicants = []
        selected_implicants = []
        missing_implicants = []
        minimal_implicants = []
        functions = []

        for x in self.miniTerms:
            table[binToHex(x)]=[]
    
        for i in self.primeImplicants:
            for j in i["hex"]:
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

        essential_implicants = [x[0] for x in essential_implicants]

        for char in mainList:
            for i in range(len(functions)):
                functions[i] = []

        for i in range (len(functions)):
            functions[i] = [x[0] for x in functions[i]]
 
        return essential_implicants, functions
   