import time
import random


operators = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]    #globalne premenne, aby bola iba jedna, lahko pristupna sachovnica
print("specify amount of rows")                                                         #input pre rozmery sachovnice
d = int(input())
board = [[0 for i in range(d)] for j in range(d)]                                       #vytvorenie sachovnice

def printBoard():                                                                       #pekny formatovany vypis stavu sachovnice
    for i in range(0,len(board)):
        for j in range(0,len(board)):
            print(board[i][j],end=" ")
            if(board[i][j]<10):
                print(" ", end=""),
        print("")

def moves(startx, starty):                                                              #tato funkcia spätne zisti, aky bol postup operatorov
    riadok = startx
    stlpec = starty
    moveStr = ""
    for i in range(2,(d*d)+1):
        for j in range(0,8):
            if ((riadok + operators[j][0])>=0 and (riadok + operators[j][0])<d and (stlpec + operators[j][1])>=0 and (stlpec + operators[j][1])<d): #zisti, ci je dany krok stale na sachovnici
                if ((board[riadok + operators[j][0]][stlpec + operators[j][1]]) == i):
                    moveStr+=str(j)
                    riadok+=operators[j][0]
                    stlpec += operators[j][1]
                    break
    print("poradie vybratých operátorov: {}\n\n".format(moveStr))

def checkMove(op, riadok, stlpec):                                          #funkcia zisti, ci je dany krok(operator) mozny, teda nevystupi zo sachovnice a nestupi na obsadene policko
    if (riadok + operators[op][0])<0 or (riadok + operators[op][0])>=d or (stlpec + operators[op][1])<0 or (stlpec + operators[op][1])>=d:
        return False            #ak vystupi zo sachovnice
    elif((board[riadok + operators[op][0]][stlpec + operators[op][1]]) == 0):
        return True                 #ak policko nie je obsadene a nevystupil zo sachovnice
    else:
        return False                #ak policko je obsadene


def iterate(key, riadok, stlpec, maxTime, finish, startTimeReal):       #rekurzivna funkcia, ktora sa stara o skoro cele hladanie riesenia
    if (time.time() - startTimeReal > maxTime and finish ==0):          #ak sa nepodarilo skoncit v casovom limite, rekurzia konci
        print("Riešenie nebolo nájdené včas")
        finish = 2
        return finish
    if(finish == 1 or finish == 2):                                     #pokracovanie vychadzania z rekurzie
        return finish
    for i in reversed(range(0,8)):                                      #v tomto pripade nechavam opacny prechod operatorov, da sa to otocit odstranenim reversed()
        if(checkMove(i, riadok, stlpec) == True):           #ak je to vyhovujuci krok
            board[riadok+operators[i][0]][stlpec+operators[i][1]] = key+1
            finish = iterate(key+1, riadok+operators[i][0], stlpec+operators[i][1], maxTime, finish, startTimeReal)
    if (key < d * d):                                       #ak rozvijanie daneho uzla skoncilo, a pritom este nie je najdene riesenie, vracia sa po svojich stopach a zahladzuje ich nulami
        board[riadok][stlpec] = 0
        return finish
    else:                                                   #ak sa najde spravne riesenie, vypise sa aktualna sachova doska a poradie krokov(operatorov)
        printBoard()
        print("success, --- %s seconds ---" % (time.time() - startTimeReal))
        for x in range(0,d):                                #tento cyklus najde policko, kde sa nachadza jednotka, a posle ho do funkcie moves() na vypisanie poradia krokov
            for y in range(0,d):
                if(board[x][y]==1):
                    moves(x,y)
        #moves()
        finish = 1
        return finish


def iterations(maxtime):                                #tato funkcia riadi volanie nasej prehladavacej funkcie podla zadania
    for a in range(0, d):                               #vynulovanie dosky, a spustenie algoritmu pre lavy dolny roh sachovnice
        for b in range(0, d):
            board[a][b] = 0
    startX = d-1
    startY = 0
    board[startX][startY] = 1
    startTimeReal = time.time()
    print("start: {}, {}".format(startX,startY))
    iterate(1, startX, startY, maxtime, 0, startTimeReal)

    for i in range(0,4):                                #vynulovanie dosky, a spustenie algoritmu pre 4 nahodne pozicie na sachovnici
        for a in range(0, d):
            for b in range(0, d):
                board[a][b] = 0
        startX = random.randint(0,d-1)
        startY = random.randint(0,d-1)
        if(d%2==1 and (startX+startY)%2==1):           #pri neexistujucom rieseni ho nema pointu hladat, no ajtak by to fungovalo, len by nenaslo dane riesenie
            print("neexistujúce riešenie pre {}, {}\n\n".format(startX,startY))
            continue
        board[startX][startY] = 1
        startTimeReal = time.time()
        print("start: {}, {}".format(startX,startY))
        iterate(1, startX, startY, maxtime, 0, startTimeReal)

print("specify time limit(seconds)")                    #input pre casovy limit hladania
maxtime = int(input())

iterations(maxtime)                                     #spustenie programu