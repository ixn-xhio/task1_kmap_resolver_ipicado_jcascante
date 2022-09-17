#convierte binary to hex
def binToHex(number):
    try:
        return int(number,2)
    except Exception as e:
        print(e)
        return

#converts hex to binary
def hexToBin(number, length):
    try:
        return format(int(number), f'0'+str(length)+'b')
    except Exception as e:
        print(e)
        return

#primera comparacion, los hexa se unen en un array
def firstCompare(group1, group2, group3, numOfVariables):
    for i in range(len(group1)):
            for j in range(len(group2)):
                count = 0
                combined = ""
                for k in range(numOfVariables):
                    combined += group1[i]["bin"][k]
                    if group1[i]['bin'][k] != group2[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group3]:
                        group3.append({
                            'bin': combined,
                            'hex': [group1[i]['hex'], group2[j]['hex']]
                        })
    return group3

#primera comparacion, los hex vienen en array asi que se mergean
def secondCompare(group1, group2, group3, numOfVariables):
    for i in range(len(group1)):
            for j in range(len(group2)):
                count = 0
                combined = ""
                for k in range(numOfVariables):
                    combined += group1[i]["bin"][k]
                    if group1[i]['bin'][k] != group2[j]['bin'][k]:
                        count += 1
                        combined = combined[:k] + "-"
                if count == 1:
                    if combined not in [x["bin"] for x in group3]:
                        group3.append({
                            'bin': combined,
                            'hex': group1[i]['hex'] + group2[j]['hex']
                        })
    return group3

#tercera comparacion
#solo se puede agregar una cuarta diferencia o quiere decir que todos los miniterminos son diferentes entre los grupos
#compara count a 3 por necesidad de 5 variables

def thirdCompare(group1, group2, group3, numOfVariables):
    for i in range(len(group1)):
            for j in range(len(group2)):
                count = 0
                combined = ""
                for k in range(numOfVariables):
                    combined += group1[i]["bin"][k]
                    if group1[i]['bin'][k] == '-' and group2[j]['bin'][k] == '-':
                        count += 1
                        combined = combined[:k] + "-"
                if count == 3:
                    if combined not in [x["bin"] for x in group3]:
                        group3.append({
                            'bin': combined,
                            'hex': group1[i]['hex'] + group2[j]['hex']
                        })
    return group3

#agrega los implicantes restantes si quedan miniterminos fuera del ultimo grupo lleno
def completePrimeImplicants(lastImplicantsGroup, missingImplicants, primeImplicants):
    for implicant in lastImplicantsGroup:
        count = 0
        for missing in missingImplicants:
            if missing not in implicant["hex"]:
                count += 1
        if count == 0:
            if(implicant["bin"] not in [x["bin"] for x in primeImplicants]):
                primeImplicants.append(implicant)
                missingImplicants = []

    for implicant in lastImplicantsGroup:
        for missing in missingImplicants:
            if missing in implicant["hex"]:
                primeImplicants.append(implicant)
                del missingImplicants[missingImplicants.index(missing)]
    return primeImplicants
