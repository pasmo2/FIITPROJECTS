import random               #potrebné pre generovanie náhodnej hodnoty z intervalu
import statistics               #potrebné pre zistenie hodnoty median z listu
import matplotlib.pyplot as plt     #potrebné pre tvorenie grafov

def initialize():                               #jednoduché načítanie parametrov na vstupe pomocou input()
    print("Zadajte počet riadkov:")
    rows=int(input())
    print("Zadajte počet stĺpcov:")
    columns=int(input())
    print("Zadajte počet génov jedného chromozómu:")
    geneCount = int(input())
    print("Vyberte typ výberu(turnaj/ruleta):")
    selection = input()
    if(selection!="turnaj" and selection!="ruleta"):
        print("nesprávny vstup")
        return
    print("Zadajte počet kameňov:")
    stoneCount=int(input())
    print("Zadajte počet generácií:")
    generationCount = int(input())
    stones = []
    for i in range(0, stoneCount):
        print("Zadajte riadkové súradnice {}. kameňa:".format(i + 1))
        stoneRow = int(input())
        print("Zadajte stĺpcové súradnice {}. kameňa:".format(i + 1))
        stoneColumn = int(input())
        stones.append([stoneRow-1,stoneColumn-1])
    mainLoop(rows, columns, stoneCount, stones, selection, geneCount, generationCount)      #zavolanie hlavnej funkcie programu
def printGarden(garden):                            #jednoduché rozdelenie a vypísanie stavu záhrady
    print("Garden: \n")
    for i in range(0,len(garden)):
        if(i!=0):
            print("")
        for j  in range(0,len(garden[0])):
            print("----",end="")
        print("")
        for j in range(0,len(garden[0])):
            if (garden[i][j] < 10 and garden[i][j] != -1):
                print(" ", end="")
            print(" {}".format(garden[i][j]),end="")
            print("|",end="")
    print("")
    for j in range(0, len(garden[0])):
        print("----", end="")
    print("\n")

def getFitness(garden):                                             #spočíta nenulové a ne-mínusjednotkové hodnoty v našej záhrade
    count = 0
    for i in range(0,len(garden)):
        for j in range(0,len(garden[0])):
            if (garden[i][j]!=0 and garden[i][j]!=-1):
                count+=1
    return count
def findCoords(pos, garden):                                        #nájde koordinácie vstupného políčka záhrady pre každý gén
    rows = len(garden)
    columns = len(garden[0])
    direction = 0
    if (pos < 1 or pos > (rows + columns) * 2):
        print("error 1")
        return -1,-1
    elif (pos >= 1 and pos <= columns):
        rowNum = 0
        colNum = pos - 1
        direction = 1
    elif (pos >= columns + 1 and pos <= 2 * columns):
        rowNum = rows - 1
        colNum = pos - (1 + columns)
        direction = 2
    elif (pos >= (2 * columns) + 1 and pos <= (2 * columns) + rows):
        rowNum = pos - (1 + (columns * 2))
        colNum = 0
        direction = 3
    elif (pos >= (2 * columns) + 1 + rows and pos <= (2 * columns) + (rows * 2)):
        rowNum = pos - (1 + (columns * 2) + rows)
        colNum = columns - 1
        direction = 4
    else:
        print("error 2")
        return -1,-1
    return rowNum, colNum, direction

def checkAvailability(garden, pos):                                         #archaická nepoužitá funkcia zanechaná pre zachovanie integrity projektu
    rowNum, colNum, direction = findCoords(pos, garden)
    if(rowNum == -1 or colNum == -1):
        return False
    if(garden[rowNum][colNum]==0):
        return True
    else:
        return False

def createGarden(rows, columns, stoneCount, stones):                #vytvorí prázdnu záhradu(iba s kameňmi)
    garden = [[0 for i in range(columns)] for j in range(rows)]
    for i in range(0,stoneCount):
        garden[stones[i][0]][stones[i][1]] = -1
    return garden

def generateGarden(chromosome, garden):                         #do prázdnej záhrady z predošlej funkcie doplní kroky mnícha podľa génov daného chromozómu
    geneNum = 20
    brick = False
    for i in range(0,geneNum):
        brick = generatePath(garden, chromosome[i], i+1)
        if(brick == True):
            #print("brick {}".format(i+1))
            break

def generatePath(garden, pos, num):                             #táto funcia ovláda chôdzu a otáčanie mnícha, ako je opísané v dokumentácii. Každý smer je napísaný manuálne.
    row, column, direction = findCoords(pos, garden)
    if(garden[row][column] != 0):
        return False
    rows = len(garden)
    columns = len(garden[0])
    able= True                                                                          #prepínače pre chod funkcie
    brick = False                                                                       #
    while(able == True):
        garden[row][column] = num
        if(direction == 1 and (row+1 >=rows or row+1<0)):
            able = False
        if (direction == 2 and (row - 1 >= rows or row - 1 < 0)):
            able = False
        if (direction == 3 and (column + 1 >= columns or column + 1 < 0)):
            able = False
        if (direction == 4 and (column - 1 >= columns or column - 1 < 0)):
            able = False
        if(direction == 1):                                                             #4 časti kódu pre 4 konkrétne smery chôdze
            if (row+1 >=0 and row+1<rows and garden[row+1][column] == 0):
                row+=1
                continue
            else:
                if(column-1 >=0 and column-1 < columns and garden[row][column-1] == 0):
                    column-=1
                    direction = 4
                    continue
                elif(column+1 >=0 and column+1 < columns and garden[row][column+1] == 0):
                    column+=1
                    direction = 3
                    continue
                else:
                    brick = True
                    able = False
        if (direction == 2):
            if (row - 1 >= 0 and row - 1 < rows and garden[row - 1][column] == 0):
                row -= 1
                continue
            else:
                if (column + 1 >= 0 and column + 1 < columns and garden[row][column + 1] == 0):
                    column += 1
                    direction = 3
                    continue
                elif (column - 1 >= 0 and column - 1 < columns and garden[row][column - 1] == 0):
                    column -= 1
                    direction = 4
                    continue
                else:
                    brick = True
                    able = False
        if (direction == 3):
            if (column + 1 >= 0 and column + 1 < columns and garden[row][column+1] == 0):
                column += 1
                continue
            else:
                if (row + 1 >= 0 and row + 1 < rows and garden[row+1][column] == 0):
                    row += 1
                    direction = 1
                    continue
                elif (row - 1 >= 0 and row - 1 < rows and garden[row - 1][column] == 0):
                    row -= 1
                    direction = 2
                    continue
                else:
                    brick = True
                    able = False
        if (direction == 4):
            if (column - 1 >= 0 and column - 1 < columns and garden[row][column-1] == 0):
                column -= 1
                continue
            else:
                if (row - 1 >= 0 and row - 1 < rows and garden[row-1][column] == 0):
                    row -= 1
                    direction = 2
                    continue
                elif (row + 1 >= 0 and row + 1 < rows and garden[row + 1][column] == 0):
                    row += 1
                    direction = 1
                    continue
                else:
                    brick = True
                    able = False
    if(row == rows-1 or row == 0 or column == columns-1 or column == 0):
        brick=False
    return brick
    
def generateRandomChromosome(numPos, rows, columns, stoneCount, stones, geneCount):             #funkcia vygeneruje chromozóm s náhodnými typmi génov(bez opakovania génov)
    chromosome = []
    for x in range(0,geneCount):
        chromosome.append(0)
    for i in range(0,geneCount):
        fine = False
        while(True):
            geneNum = random.randint(1, numPos)
            finecount = 0
            for y in range(0,i):
                if(chromosome[y]==geneNum):
                    finecount = 1
            if(finecount == 0):
                break
        chromosome[i] = geneNum
    return chromosome

def genChrom(unitCount, numPos, rows, columns, stoneCount, stones, geneCount):                              #funkcia sa stará o chod predošlej funkcie a spravovanie vlastností daných chromozómov(fitness, pridanie do listu/generácie)
    generation = []
    fitness = []
    for i in range(0,unitCount):
        chromosome = generateRandomChromosome(numPos, rows, columns, stoneCount, stones, geneCount)
        generation.append(chromosome)
        garden = createGarden(rows, columns, stoneCount, stones)
        generateGarden(chromosome, garden)
        singleFitness = getFitness(garden)
        fitness.append(singleFitness)
    return generation, fitness
def mutation(chromosome, geneCount, numPos):                                            #táto funkcia sa stará o mutáciu chromozómu - náhodnú zmenu génu
    rollGene = random.randint(1,numPos)
    rollGeneIndex =  random.randint(0,geneCount-1)
    chromosome[rollGeneIndex] = rollGene
    return chromosome

def rouletteSelection(fullRoulette, fitness, generation):               #vyberie podla nahodnej hodnoty jedneho jedinca, pricom vyssi fitness == vyssia sanca
    done = 0
    med = statistics.median(fitness)
    while(done == 0):
        select = random.randint(0, fullRoulette)
        for i in range(0,len(fitness)):
            if(select<=fitness[i]):
                roll = random.randint(1,3)
                if(fitness[i] < med and roll == 1):
                    done = 1
                    return generation[i]
                elif(fitness[i]>=med):
                    done = 1
                    return generation[i]
            else:
                select -= fitness[i]
    #print("error 3")
    return None
def firstPhase(unitCount, generation, fitness):                 #vyberie 10% najlepsich jedincov do dalsej generacie
    bestCount = int(unitCount/100*10)
    newGen = []
    newGenFitness = []
    for i in range(0, bestCount):
        idx = fitness.index(max(fitness))
        newGen.append(generation[idx])
        newGenFitness.append(fitness[idx])
        #fitness.pop(idx)
        #generation.pop(idx)
    return newGen, newGenFitness

def secondPhase(unitCount, generation, fitness, selection, geneCount, rows, columns, stoneCount, stones, numPos):           #vytvori 70% novych krizenych jedincov do dalsej generacie
    secondCount = int(unitCount/100*70)
    chanceOfMutation = 10            #percent
    mutationRoll = random.randint(1,100)
    newGen = []
    newGenFitness = []
    if(selection == "ruleta"):                                                  #vyber rodicov pre ruletu, potom vytvorenie noveho jedinca
        fullRoulette = 0
        for a in range(0,len(fitness)):
            fullRoulette+=fitness[a]
        for i in range(0, secondCount):
            firstParent = rouletteSelection(fullRoulette, fitness, generation)
            secondParent = rouletteSelection(fullRoulette, fitness, generation)
            roll = random.randint(0,geneCount)
            newChrom = []
            for x in range(0,roll):
                newChrom.append(firstParent[x])
            for y in range(roll,geneCount):
                newChrom.append(secondParent[y])
            if(mutationRoll<=chanceOfMutation):
                newChrom = mutation(newChrom, geneCount, numPos)
            garden = createGarden(rows, columns, stoneCount, stones)
            generateGarden(newChrom, garden)
            singleFitness = getFitness(garden)
            newGen.append(newChrom)
            newGenFitness.append(singleFitness)
        return newGen,newGenFitness
    if(selection == "turnaj"):                                  #pri turnaji sa lisi iba vyber rodicov, tvorenie noveho jedinca krizenim je rovnake
        for i in range(0,secondCount):
            turnajRoll1 = random.randint(0, len(fitness) - 1)
            turnajRoll2 = random.randint(0, len(fitness) - 1)
            turnajRoll3 = random.randint(0, len(fitness) - 1)
            turnajPick = [fitness[turnajRoll1], fitness[turnajRoll2], fitness[turnajRoll3]]
            maks = max(turnajPick)
            if(maks== fitness[turnajRoll1]):
                myPick = turnajRoll1
            elif(maks== fitness[turnajRoll2]):
                myPick = turnajRoll2
            else:
                myPick = turnajRoll3
            firstParent = generation[myPick]
            turnajRoll1 = random.randint(0, len(fitness) - 1)
            turnajRoll2 = random.randint(0, len(fitness) - 1)
            turnajRoll3 = random.randint(0, len(fitness) - 1)
            turnajPick = [fitness[turnajRoll1], fitness[turnajRoll2], fitness[turnajRoll3]]
            maks = max(turnajPick)
            if (maks == fitness[turnajRoll1]):
                myPick = turnajRoll1
            elif (maks == fitness[turnajRoll2]):
                myPick = turnajRoll2
            else:
                myPick = turnajRoll3
            secondParent = generation[myPick]

            roll = random.randint(0, geneCount)
            newChrom = []
            for x in range(0, roll):
                newChrom.append(firstParent[x])
            for y in range(roll, geneCount):
                newChrom.append(secondParent[y])
            if (mutationRoll <= chanceOfMutation):
                newChrom = mutation(newChrom, geneCount, numPos)
            garden = createGarden(rows, columns, stoneCount, stones)
            generateGarden(newChrom, garden)
            singleFitness = getFitness(garden)
            newGen.append(newChrom)
            newGenFitness.append(singleFitness)
        return newGen, newGenFitness



def mainLoop(rows, columns, stoneCount, stones, selection, geneCount, generationCount):         #hlavna funkcia programu, ktora ovlada cely chod algoritmu
    unitCount = 100                                         #pocet jedincov v jednej generacii
    numPos = (rows+columns)*2                               #pocet roznych genov
    maxlist = []
    medlist = []
    if(geneCount > rows+columns+stoneCount or geneCount< 1):
        print("Zadaný nesprávny počet génov")
        return
    generation, fitness = genChrom(unitCount, numPos, rows, columns, stoneCount, stones, geneCount)     #vytvorenie prvej generacie
    print("max fitness 1. generacie: {}".format(max(fitness)))
    for i in range(0,generationCount):                                                                  #loop s tvorenim novych generacii
        newGen, newGenFitness = firstPhase(unitCount, generation, fitness)                      #prva faza
        secondPhaseGen, secondPhaseFitness = secondPhase(unitCount, generation, fitness, selection, geneCount, rows, columns, stoneCount, stones, numPos)           #druha faza
        for j in range(0, len(secondPhaseGen)):
            newGen.append(secondPhaseGen[j])
            newGenFitness.append(secondPhaseFitness[j])
        thirdPhaseGen, thirdPhaseFitness = genChrom(int(unitCount/100*20), numPos, rows, columns, stoneCount, stones, geneCount)            #tretia faza
        for k in range(0, len(thirdPhaseGen)):
            newGen.append(thirdPhaseGen[k])
            newGenFitness.append(thirdPhaseFitness[k])
        generation = newGen                         #prenesenie novo vytvorenych jedincov do novej(aktualnej) generacie
        fitness = newGenFitness
        maxlist.append(max(fitness))                #tvorenie listov pre grafy
        medlist.append(statistics.median(fitness))
        if(i> 0 and i%100==0):                              #vypis maximalnej hodnoty fitness pre kazdu 100tu generaciu
            print("max fitness {}. generacie: {}".format(i, max(fitness)))
        if(max(fitness) == (rows*columns)-stoneCount):                          #vypis pre uspesne riesenie - vypis zahrady a grafov
            print("našlo sa riešenie v {}. generacií:".format(i))
            garden = createGarden(rows, columns, stoneCount, stones)            #vytvorenie a vypisanie finalnej zahrady
            generateGarden(generation[fitness.index(max(fitness))], garden)
            printGarden(garden)
            plt.plot(range(len(maxlist)), maxlist)                          #vytvorenie grafov
            plt.xlabel("Číslo generácie")
            plt.ylabel("Maximálna hodnota fitness")
            plt.show()
            plt.plot(range(len(medlist)), medlist)
            plt.xlabel("Číslo generácie")
            plt.ylabel("Stredná hodnota fitness")
            plt.show()
            return
    print("Nepodarilo sa nájsť kompletnú cestu.\nV poslednej generácii bola najvyššia hodnota fitness {}.".format(max(fitness)))            #vypis pre neuspesne riesenie
initialize()
