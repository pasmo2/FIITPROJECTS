import random
import matplotlib.pyplot as plt
import numpy as np
import math
import time

def sortByDistance(point):                                                      #funkcia potrebna pre sortovanie listu distances podla vzdialenosti
    return point[0]
def createPoint(x,y,clxss, clxss1, clxss3, clxss7, clxss15):                                                 #funkcia vytvori bod so suradnicami a jeho triedami
    point = [x,y, clxss, clxss1, clxss3, clxss7, clxss15]
    return point
def fiveStartingPoints(xop, yop, points):                               #vytvorenie zaciatocnych bodov
    if(xop == "minus" and yop == "minus"):
        points.append(createPoint(-4500, -4400,"red", "red", "red", "red", "red"))
        points.append(createPoint(-4100, -3000,"red", "red", "red", "red", "red"))
        points.append(createPoint(-1800, -2400,"red", "red", "red", "red", "red"))
        points.append(createPoint(-2500, -3400,"red", "red", "red", "red", "red"))
        points.append(createPoint(-2000, -1400,"red", "red", "red", "red", "red"))
    elif (xop == "plus" and yop == "minus"):
        points.append(createPoint(+4500, -4400,"green", "green", "green", "green", "green"))
        points.append(createPoint(+4100, -3000,"green", "green", "green", "green", "green"))
        points.append(createPoint(+1800, -2400,"green", "green", "green", "green", "green"))
        points.append(createPoint(+2500, -3400,"green", "green", "green", "green", "green"))
        points.append(createPoint(+2000, -1400,"green", "green", "green", "green", "green"))
    elif (xop == "minus" and yop == "plus"):
        points.append(createPoint(-4500, +4400,"blue", "blue", "blue", "blue", "blue"))
        points.append(createPoint(-4100, +3000,"blue", "blue", "blue", "blue", "blue"))
        points.append(createPoint(-1800, +2400,"blue", "blue", "blue", "blue", "blue"))
        points.append(createPoint(-2500, +3400,"blue", "blue", "blue", "blue", "blue"))
        points.append(createPoint(-2000, +1400,"blue", "blue", "blue", "blue", "blue"))
    elif (xop == "plus" and yop == "plus"):
        points.append(createPoint(+4500, +4400,"purple", "purple", "purple", "purple", "purple"))
        points.append(createPoint(+4100, +3000,"purple", "purple", "purple", "purple", "purple"))
        points.append(createPoint(+1800, +2400,"purple", "purple", "purple", "purple", "purple"))
        points.append(createPoint(+2500, +3400,"purple", "purple", "purple", "purple", "purple"))
        points.append(createPoint(+2000, +1400,"purple", "purple", "purple", "purple", "purple"))
def initializePoints():                                 #vytvorenie zaciatocnych bodov po piatich
    points = []
    splinters = [[[] for _ in range(5)] for _ in range(5)]
    fiveStartingPoints("minus", "minus", points)
    fiveStartingPoints("plus", "minus", points)
    fiveStartingPoints("minus", "plus", points)
    fiveStartingPoints("plus", "plus", points)
    for i in range(0,len(points)):
        x,y=findSplinter(points[i][0],points[i][1])
        splinters[x][y].append(points[i])

    return points,splinters
def findSplinter(x,y):                      #funkcia najde k bodu jeho prislusnu podplochu/podlist
    x+=5000
    y+=5000
    xn = int(x/2000)
    if(xn==5):
        xn=4
    yn = int(y / 2000)
    if(yn==5):
        yn=4
    return xn,yn
def createSplinter(point, splinters):       #funkcia prida bod do listu s 25 podplochami
    x,y = findSplinter(point[0],point[1])
    splinters[x][y].append(point)
def checkPoint(points, x, y, splinters):                    #zistenie, ci je vygenerovany bod unikatny
    a,b = findSplinter(x,y)
    for i in range(0,len(splinters[a][b])):
        if(splinters[a][b][i][0] == x and splinters[a][b][i][1] == y):
            return False
    return True
    #for i in range(0,len(points)):
    #    if(points[i][0] == x and points[i][1] == y):
    #        return False
    #return True
def generateFourPoints(points, splinters, classifications, success):                            #funkcia, ktora sa stara o generovanie novych bodov(po stvoriciach)
    roll = random.randint(1,100)                    #rollnutie, ci mame generovat body v danom intervale alebo nie
    if(roll!=1):                                #generujeme v intervale
        while(True):
            xroll = random.randint(-5000,500)
            yroll = random.randint(-5000,500)
            if(checkPoint(points,xroll,yroll, splinters) == True):                      #ak je vygenerovany bod unikatny
                newpoint = createPoint(xroll,yroll,"red","red","red","red","red")
                classify(splinters, newpoint, classifications)                                          #klasifikacia bodu
                newpoint[3] = classifications[len(classifications) - 1][3]                          #nastavenie novych tried
                newpoint[4] = classifications[len(classifications) - 1][4]
                newpoint[5] = classifications[len(classifications) - 1][5]
                newpoint[6] = classifications[len(classifications) - 1][6]
                if(newpoint[2]==newpoint[3]):                                               #ak je bod uspesne klasifikovany rovnako ako bol pociatocne, inkrementuje sa pocitadlo
                    success[0]+=1
                if (newpoint[2] == newpoint[4]):
                    success[1] += 1
                if (newpoint[2] == newpoint[5]):
                    success[2] += 1
                if (newpoint[2] == newpoint[6]):
                    success[3] += 1
                points.append(newpoint)                                                 #pridanie noveho bodu do listu s bodmi
                createSplinter(newpoint,splinters)                                      #a takisto aj do listu podploch
                break
        while (True):                                                                   #tento while loop sa opakuje 4 krat, teda raz pre kazdu triedu, a este raz pre generaciu bodov mimo intervalu
            xroll = random.randint(-500, 5000)
            yroll = random.randint(-5000, 500)
            if (checkPoint(points, xroll, yroll, splinters) == True):
                newpoint = createPoint(xroll, yroll, "green", "green", "green", "green", "green")
                classify(splinters, newpoint, classifications)
                newpoint[3] = classifications[len(classifications) - 1][3]
                newpoint[4] = classifications[len(classifications) - 1][4]
                newpoint[5] = classifications[len(classifications) - 1][5]
                newpoint[6] = classifications[len(classifications) - 1][6]
                if (newpoint[2] == newpoint[3]):
                    success[0] += 1
                if (newpoint[2] == newpoint[4]):
                    success[1] += 1
                if (newpoint[2] == newpoint[5]):
                    success[2] += 1
                if (newpoint[2] == newpoint[6]):
                    success[3] += 1
                points.append(newpoint)
                createSplinter(newpoint, splinters)
                break
        while (True):
            xroll = random.randint(-5000, 500)
            yroll = random.randint(-500, 5000)
            if (checkPoint(points, xroll, yroll, splinters) == True):
                newpoint = createPoint(xroll, yroll, "blue", "blue", "blue", "blue", "blue")
                classify(splinters, newpoint, classifications)
                newpoint[3] = classifications[len(classifications) - 1][3]
                newpoint[4] = classifications[len(classifications) - 1][4]
                newpoint[5] = classifications[len(classifications) - 1][5]
                newpoint[6] = classifications[len(classifications) - 1][6]
                if (newpoint[2] == newpoint[3]):
                    success[0] += 1
                if (newpoint[2] == newpoint[4]):
                    success[1] += 1
                if (newpoint[2] == newpoint[5]):
                    success[2] += 1
                if (newpoint[2] == newpoint[6]):
                    success[3] += 1
                points.append(newpoint)
                createSplinter(newpoint, splinters)
                break
        while (True):
            xroll = random.randint(-500, 5000)
            yroll = random.randint(-500, 5000)
            if (checkPoint(points, xroll, yroll, splinters) == True):
                newpoint = createPoint(xroll, yroll, "purple", "purple", "purple", "purple", "purple")
                classify(splinters, newpoint, classifications)
                newpoint[3] = classifications[len(classifications) - 1][3]
                newpoint[4] = classifications[len(classifications) - 1][4]
                newpoint[5] = classifications[len(classifications) - 1][5]
                newpoint[6] = classifications[len(classifications) - 1][6]
                if (newpoint[2] == newpoint[3]):
                    success[0] += 1
                if (newpoint[2] == newpoint[4]):
                    success[1] += 1
                if (newpoint[2] == newpoint[5]):
                    success[2] += 1
                if (newpoint[2] == newpoint[6]):
                    success[3] += 1
                points.append(newpoint)
                createSplinter(newpoint, splinters)
                break
    else:                                       #generovanie bodov mimo intervalu v zadani, 1% sanca, inak sa deje vsetko rovnako ako v predoslych loopoch
        for i in range(0,4):
            if(i == 0):
                clxss = "red"
            elif(i==1):
                clxss = "green"
            elif (i == 2):
                clxss = "blue"
            else:
                clxss = "purple"
            while(True):
                xroll = random.randint(-5000,5000)
                yroll = random.randint(-5000,5000)
                if(checkPoint(points,xroll,yroll, splinters) == True):
                    newpoint = createPoint(xroll,yroll,clxss,clxss,clxss,clxss,clxss)
                    classify(splinters, newpoint, classifications)
                    newpoint[3] = classifications[len(classifications) - 1][3]
                    newpoint[4] = classifications[len(classifications) - 1][4]
                    newpoint[5] = classifications[len(classifications) - 1][5]
                    newpoint[6] = classifications[len(classifications) - 1][6]
                    if (newpoint[2] == newpoint[3]):
                        success[0] += 1
                    if (newpoint[2] == newpoint[4]):
                        success[1] += 1
                    if (newpoint[2] == newpoint[5]):
                        success[2] += 1
                    if (newpoint[2] == newpoint[6]):
                        success[3] += 1
                    points.append(newpoint)
                    createSplinter(newpoint, splinters)
                    break
def generateNewPoints(points, splinters, iterations, classifications):                  #funkcia zavola generovaciu funkciu n krat, podla premennej iterations
    success = [0,0,0,0]
    for i in range(0,iterations):
        generateFourPoints(points, splinters, classifications, success)
    return success
def getDistance(pointA, pointB):                                                        #funkcia vrati vzdialenost medzi danymi bodmi
    diffX = pointA[0] - pointB[0]
    diffY = pointA[1] - pointB[1]
    dist2 = ((diffX**2) + (diffY**2))
    dist = math.sqrt(dist2)
    return dist
def checkIfUnique(splinters, newsplinter):                                #funkcia sluzi na osetrenie pridavania rovnakych podploch do vyberu pre zoradenie vzdialenosti
    for i in range(0,len(splinters)):
        if(splinters[i]==newsplinter):
            return False
    return True
def classifyFinal(distances, clxss, n):             #druha cast klasifikacie
    n -= 1                  #index pre dane k v liste distances
    r = 0                   #pocty vyskytov danych tried
    g = 0
    b = 0
    p = 0
    for i in range(0,len(distances)):                   #spocitaju sa vyskyty tried
        if (distances[i][n] == "red"):
            r += 1
        if (distances[i][n] == "green"):
            g += 1
        if (distances[i][n] == "blue"):
            b += 1
        if (distances[i][n] == "purple"):
            p += 1
    counts = [r, g, b, p]
    maximum = max(counts)
    maxcounts = []
    for i in range(0,len(counts)):                                  #vsetky triedy, ktore maju najvyssi pocet vyskytov v KNN, sa pridaju do listu maxcounts
        if(counts[i]==maximum):
            if (i == 0):
                maxcounts.append("red")
            if (i == 1):
                maxcounts.append("green")
            if (i == 2):
                maxcounts.append("blue")
            if (i == 3):
                maxcounts.append("purple")
    found = 0
    classifiedAs = 0
    for i in range(0,len(distances)):                   #z tried v maxcounts sa vyberie prvy vyskyt danej triedy v liste distances, teda najblizsi bod s danou triedou
        for j in range(0,len(maxcounts)):
            if(distances[i][n] == maxcounts[j]):
                found = 1
                classifiedAs = maxcounts[j]
                break
        if(found == 1):
            break

    return classifiedAs

    #if(classifiedAs == 0):
    #    print("error 2 --------------------------------------")
    #if(classifiedAs == clxss):
    #    return 1
    #else:
    #    return 0

def classify(splinters, point, classifications):
    x, y = findSplinter(point[0],point[1])
    relevantSplinters = []
    relevantSplinters.append(splinters[x][y])
    if (x - 1 >= 0 and x - 1 <= 4):                                                      #najdem vsetky okolite splintery, bruteforce neinteligentne spracovanie
        if(checkIfUnique(relevantSplinters, splinters[x-1][y])==True):      #zistim, ci sa dany splinter uz nachadza v relevantnych splinteroch
            relevantSplinters.append(splinters[x - 1][y])
        if(y-1>=0 and y-1<=4):                                                      #osetrim vystupovanie z listu
            if (checkIfUnique(relevantSplinters, splinters[x - 1][y-1]) == True):                                   #tento proces sa deje po trojiciach policok v kazdom smere, teda 4 krat 3
                relevantSplinters.append(splinters[x - 1][y - 1])
        if (y + 1 >= 0 and y + 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x - 1][y+1]) == True):
                relevantSplinters.append(splinters[x - 1][y + 1])
    if (x + 1 >= 0 and x + 1 <= 4):
        if (checkIfUnique(relevantSplinters, splinters[x + 1][y]) == True):
            relevantSplinters.append(splinters[x + 1][y])
        if (y - 1 >= 0 and y - 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x + 1][y-1]) == True):
                relevantSplinters.append(splinters[x + 1][y - 1])
        if (y + 1 >= 0 and y + 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x + 1][y+1]) == True):
                relevantSplinters.append(splinters[x + 1][y + 1])
    if (y + 1 >= 0 and y + 1 <= 4):
        if (checkIfUnique(relevantSplinters, splinters[x][y+1]) == True):
            relevantSplinters.append(splinters[x][y + 1])
        if (x - 1 >= 0 and x - 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x - 1][y+1]) == True):
                relevantSplinters.append(splinters[x - 1][y + 1])
        if (x + 1 >= 0 and x + 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x + 1][y+1]) == True):
                relevantSplinters.append(splinters[x + 1][y + 1])
    if (y - 1 >= 0 and y - 1 <= 4):
        if (checkIfUnique(relevantSplinters, splinters[x][y-1]) == True):
            relevantSplinters.append(splinters[x][y - 1])
        if (x - 1 >= 0 and x - 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x - 1][y-1]) == True):
                relevantSplinters.append(splinters[x - 1][y - 1])
        if (x + 1 >= 0 and x + 1 <= 4):
            if (checkIfUnique(relevantSplinters, splinters[x - 1][y]) == True):
                relevantSplinters.append(splinters[x - 1][y])


    distances = []                                      #relevantne podplochy pridam do listu distances
    for i in range(0,len(relevantSplinters)):
        for j in range(0,len(relevantSplinters[i])):                                #pridam vzdialenosti
            distances.append([getDistance(point, relevantSplinters[i][j]), relevantSplinters[i][j][2], relevantSplinters[i][j][3], relevantSplinters[i][j][4], relevantSplinters[i][j][5], relevantSplinters[i][j][6]])

    distances.sort(key=sortByDistance)                          #tento list usporiadam podla vzdialenosti

    #print("point coords: {}, {}".format(point[0]+5000,point[1]+5000))
    #for i in range(0,len(distances)):
    #    print(distances[i])
    #print("----------------------------------------------")
    k=1                                                                                     #4x opakujem proces -> nastavim k, osetrim vynimky, zavolam funkciu ktora dokonci klasifikaciu
    if(len(distances)<k):
        if (len(distances) == 0):
            print("error 1-----------------------------------------------------------")
        k=len(distances)
    result1 = classifyFinal(distances[:k], point[3], 3)
    k=3
    if (len(distances) < k):
        if (len(distances) == 0):
            print("error 1-----------------------------------------------------------")
        k = len(distances)
    result3 = classifyFinal(distances[:k], point[4], 4)
    k=7
    if (len(distances) < k):
        if (len(distances) == 0):
            print("error 1-----------------------------------------------------------")
        k = len(distances)
    result7 = classifyFinal(distances[:k], point[5], 5)
    k=15
    if (len(distances) < k):
        if (len(distances) == 0):
            print("error 1-----------------------------------------------------------")
        k = len(distances)
    result15 = classifyFinal(distances[:k], point[6], 6)


    classifications.append([point[0],point[1],point[2],result1,result3,result7,result15])           #pridanie novoziskanych dat o klasifikacii do listu


    #return result

def mainLoop(n):
    starttime = time.time()
    classifications = []
    points,splinters = initializePoints()                           #volam funkciu, ktora inicializuje body
    success = generateNewPoints(points, splinters, n, classifications)      #volam funkciu, ktora vygeneruje nove body a klasifikuje ich
    elapsedtime = time.time() - starttime
    print("time elapsed: {}s".format(elapsedtime))
    success1 = (success[0] / (n * 4)) * 100                         #vypocitam uspenost v percentach
    success2 = (success[1] / (n * 4)) * 100
    success3 = (success[2] / (n * 4)) * 100
    success4 = (success[3] / (n * 4)) * 100

    data1 = np.array(classifications)                                                           #4x vykreslim graf->x,y ostavaju pre body rovnake, meni sa farba klasifikacie
    x = data1.transpose()[0]
    y = data1.transpose()[1]
    color = data1.transpose()[3]
    x = x.astype(int)
    y = y.astype(int)
    plt.scatter(x, y, c=color)
    plt.title(label="k= 1, time= {:.2f}s, success rate: {:.2f}%".format(elapsedtime,success1))
    plt.show()

    color = data1.transpose()[4]
    plt.scatter(x, y, c=color)
    plt.title(label="k= 3, time= {:.2f}s, success rate: {:.2f}%".format(elapsedtime, success2))
    plt.show()

    color = data1.transpose()[5]
    plt.scatter(x, y, c=color)
    plt.title(label="k= 7, time= {:.2f}s, success rate: {:.2f}%".format(elapsedtime, success3))
    plt.show()

    color = data1.transpose()[6]
    plt.scatter(x, y, c=color)
    plt.title(label="k= 15, time= {:.2f}s, success rate: {:.2f}%".format(elapsedtime, success4))
    plt.show()

print("Zadajte počet vygenerovaných bodov(z každej triedy):")                       #vypytam si vstup
num = int(input())
mainLoop(num)                                                                       #zapnem hlavny riadiaci algoritmus
