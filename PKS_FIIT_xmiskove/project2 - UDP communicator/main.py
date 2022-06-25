import random
import socket
import sys
import time
import zlib         #tu patri crc32, ktory pouzivam na kontrolu chyb v prenesenych datach

#flags
ACK = 2
ERR = 4
SEND = 8


seqandflagsize = 1                                      #7+1
checksumSize = 4                                        #crc32->32bit->4byte
headersize = checksumSize + seqandflagsize        #1byte = 7bitov flag a 1 bit sequence number ----------      flag 7 najvyssich bitov, seq number posledny 1 bit(2^0)
maxlength = 1500-20-8-headersize                    #1472-5=1467


def setFlagAndSeqNum(flag, seq):            #jednoducho setnem flagy podla ich specifickych hodnot, tento 1 byte reprezentuje hodnotu flagu+seq number
    if (flag == "ACK"):
        flag = ACK
    elif (flag == "ERR"):
        flag = ERR
    elif (flag == "SEND"):
        flag = SEND

    combined = int(flag+seq).to_bytes(seqandflagsize, "big")
    return combined

def getFlagAndSeqNum(bytesss):                  #getnem flagy a seq number opacnym sposobom ako som ich setoval, jednoducho zistim seq num podla delitelnosti dvojkou, a flag je ostatok
    num = int.from_bytes(bytesss, "big")
    seq = num % 2
    num = num - seq
    if (num == ACK):
        flag = "ACK"
    elif (num == ERR):
        flag = "ERR"
    elif (num == SEND):
        flag = "SEND"
    else:
        flag = "IDKBRO"

    return flag, seq

def getFileName(str):                           #z absolutnej cesty zisti nazov suboru, teda najde posledne lomitko a vrati chary za nim
    lastslash = 0
    for i in range(0,len(str)):
        if(str[i]=="/"):
            lastslash = i
    filename = ""
    for x in range(lastslash+1,len(str)):
        filename = filename + (str[x])
    return filename

def splitIntoFragments(maxFragment, data):                      #tato funkcia rozdeli cely subor/spravu do fragmentov podla maximalnej velkosti fragmentu
    allFragments = []
    if(len(data)>maxFragment):                                  #ak bude viac fragmentov
        fragmentCount = int(len(data)/maxFragment)
        if(len(data)%maxFragment!=0):
            fragmentCount+=1
        for i in range(0,fragmentCount):
            if(i == fragmentCount-1):
                fragmentData = data[(maxFragment * (i)):len(data)]
            else:
                fragmentData = data[(maxFragment*(i)):(maxFragment*(i+1))]
            checksum = zlib.crc32(fragmentData).to_bytes(checksumSize, "big")           #pouzitie crc32 checksumu na detekciu chyb
            flagAndSeq = setFlagAndSeqNum("SEND", i % 2)
            fragment = bytes("", encoding = "utf-8") + checksum + flagAndSeq + fragmentData         #setnutie fragmentu-> sklada sa z hlavicky(checksum+flag+seq) a dat
            allFragments.append(fragment)
    else:                                                   #ak bude iba 1 fragment
        checksum = zlib.crc32(data).to_bytes(checksumSize,"big")
        flagAndSeq = setFlagAndSeqNum("SEND", 0)
        fragment = bytes("", encoding = "utf-8") + checksum + flagAndSeq + data                 #setnutie fragmentu ako vyssie
        allFragments.append(fragment)



    return allFragments

def createInitializationPacket(dataSize, fragmentCount, pathDest):                  #vytvorenie inicializacneho packetu, pozostava z checksumu, velkosti prenasanych dat, poctu fragmentov a flagu
    firstpacket = bytes("",encoding = "utf-8") + dataSize.to_bytes(3,"big") + fragmentCount.to_bytes(3,"big") + int(35).to_bytes(1,"big") + pathDest
    initPacket = bytes("",encoding = "utf-8") + zlib.crc32(firstpacket).to_bytes(4, "big") + dataSize.to_bytes(3,"big") + fragmentCount.to_bytes(3,"big") + int(35).to_bytes(1,"big") + pathDest
    # initPacket == 4B checksum, 3B dataSize, 3B fragmentCount, 1B flag, ???B pathDest
    return initPacket

def serverSocket(ip, port):                                         #funkcia, ktora sa stara o chod serveru
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                    #vytvorenie socketu, bindnutie socketu
    server_socket.bind((ip, port))

    fragmentSize = 0                                                                    #pomocna premenna iba pre vypis potrebny v zadani

    while (True):                                                                       #hlavny loop, ktory sa stara o transfer sprav/suborov ako celkov
        successfulFragments = 0                                                         #pocet uspesne prijatych fragmentov
        fullData = bytes("",encoding = "utf-8")

        initPacket, address = server_socket.recvfrom(1500)                              #prijatie inicializacneho packetu

        if(initPacket == bytes("koniecnasejkomunikacieahoj",encoding="utf-8")):         #ak znaci ukoncenie komunikacie a serveru
            server_socket.sendto(bytes("koniecnasejkomunikacieahoj",encoding = "utf-8"), address)
            print("server ukonceny")
            break

        isFile = 0
        path = initPacket[11:].decode("utf-8")                                          #absolutna cesta k suboru
        if(path != ""):
            isFile = 1                                                                  #urcenie, ci je posielany subor alebo sprava(prazdny path = sprava)
        fragmentCount = int.from_bytes(initPacket[7:10], "big")
        checksumReceived = int.from_bytes(initPacket[0:checksumSize], "big")                #checknutie checksumu
        newChecksum = int(zlib.crc32(initPacket[checksumSize:]))
        if (checksumReceived == newChecksum and int.from_bytes(initPacket[10:11], "big") == 35):            #ak pride spravny inicializacny packet, transfer moze pokracovat
            print("inicializacny packet uspesne prijaty!\nvelkost dat: {}, pocet fragmentov: {}, path: {}".format(int.from_bytes(initPacket[4:7], "big"), int.from_bytes(initPacket[7:10], "big"), initPacket[11:].decode("utf-8")))
            server_socket.sendto(bytes("inicializacny packet bol spravne prijaty!!", encoding = "utf-8"), address)
        else:                                                                           #ak nepride spravny inicializacny packet
            print("inicializacny packet nebol uspesne prijaty, koncim loop.")
            server_socket.sendto(bytes("ERROR: inicializacny packet nebol spravne prijaty!!", encoding = "utf-8"), address)
            continue


        while(True):                                                        #loop, ktory sa stara o transfer jednotlivych fragmentov
            fragment, address = server_socket.recvfrom(1500)                    #dostaneme fragment
            if(successfulFragments==0):
                fragmentSize = 0

            if (fragment == bytes("transferover", encoding="utf-8")):                           #ak znaci koniec, konci sa transfer fragmentov
                server_socket.sendto(bytes("transferoverindeed", encoding="utf-8"), address)
                print("TRANSFER OVER\n\n")
                break

            data = fragment[headersize:]                            #data sa nachadzaju za headerom

            flag, seq = getFlagAndSeqNum(fragment[checksumSize:headersize])             #skontroluje sa flag, nizsie sa bude kontrolovat aj sequence number

            if(flag != "SEND"):                                 #ak je nespravny flag, vypyta sa fragment znova
                print("error 1, wrong flag")
                message = setFlagAndSeqNum("ERR", (seq+ 1 ) % 2)
                server_socket.sendto(message, address)
                continue

            print("Poradie prijatého fragmentu: {}".format(successfulFragments+1))


            checksumReceived = int.from_bytes(fragment[0:checksumSize], "big")                      #checkne sa checksum
            newChecksum = int(zlib.crc32(data))
            if(checksumReceived != newChecksum):                            #ak nesedi checksum, vypytam si fragment znova
                print("-------!checksum nesedi! vypytam si znova rovnaky fragment------")
                message = setFlagAndSeqNum("ERR", (seq + 1) % 2)
                server_socket.sendto(message, address)
            elif(seq != successfulFragments % 2):                                   #ak nesedi sequence number, fragment uz mam(lebo bolo oneskorenie na predoslom ACKU)
                print("---------tento fragment uz prisiel, discardne sa---------")
                message = setFlagAndSeqNum("ACK", (seq + 1) % 2)
                server_socket.sendto(message, address)
            else:                                                           #ak vsetko sedi, fragment som uspesne prijal a mozem si z neho postupne poskladat celu spravu/subor
                successfulFragments+=1
                if(successfulFragments == 1):
                    fragmentSize = len(fragment)
                print("fragment bol preneseny bez chyb")
                #print(str(data))
                fullData = fullData + data
                message = setFlagAndSeqNum("ACK", (seq + 1) % 2)
                server_socket.sendto(message, address)
                if (successfulFragments == fragmentCount):
                    print("vsetky fragmenty sa stastne dostali kam mali\n")
                    #break
            #print("sizeof data:{}, sizeof checksum: {}".format(sys.getsizeof(myPacket.data), sys.getsizeof(myPacket.header.checksum)))


        if(fragmentCount==1):                                                   #vypis informacii pozadovanych v zadani
            print("velkost packetu: {}".format(fragmentSize+32))
        else:
            print("max velkost packetov: {}".format(fragmentSize+32))
        if(isFile == 0):
            print("cela sprava: {}\n\n".format(fullData.decode("utf-8")))
        elif(isFile == 1):                              #vypis a ulozenie suboru
            fileName = getFileName(path)
            f = open(path, "wb")
            f.write(fullData)
            print("filename: {}, destination path: {}".format(fileName,path))
            f.close()

def clientSocket(ip, port):                                     #funkcia, ktora sa stara o chod klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                #vytvorenie socketu
                                                                                                                #vypytanie si vsetkych potrebnych vstupov...
    print("zadajte maximalnu velkost fragmentu(v bytoch, ciste data ktore sa prenesu)(nebude vacsia ako maximalna velkost(maxlength-32)):")
    maxFragment = int(input())
    if(maxFragment>maxlength-32):                       #ak prevysuje maximalnu velkost
        maxFragment = maxlength-32
    if(maxFragment<=0):                                         #ak je to menej ako 1byte, nastavi sa rovno na 5 bytov
        print("zadany max fragment size bol prilis maly na prenos dat, prenastavil sa na prenos aspon 5 bytov")
        maxFragment = 5


    while(True):                                                            #loop, ktory sa stara o posielanie sprav/suborov ako celku, nizsie je loop ktory sa stara o posielanie konkretnych fragmentov
        pathSrc, pathDest = "", ""
        simError, errorFragIndex = 0, 0                                 #simerror = ci budem robit s chybou, errorfragindex = index poskodeneho fragmentu
        print("vyberte si medzi spravou alebo suborom(sprava/subor):")                  #znova potrebne inputy.....
        choice = input()
        print("vyberte si, ci chcete simulovat chybu vo fragmente(y/n):")
        simChoice = input()
        if(simChoice == "y"):
            simError = 1
            print("zadajte index fragmentu, v ktorom chcete simulovat chybu")
            errorFragIndex = int(input())
        if(choice == "sprava"):
            print("zadajte spravu:")
            data = bytes(input(), encoding="utf-8")
        elif(choice == "subor"):
            print("zadajte absolutnu cestu k zdrojovemu suboru:")
            pathSrc = input()
            print("zadajte absolutnu cestu k cielovemu suboru:")
            pathDest = input()

            pathDest = pathDest.replace("\\","/")               #upravenie cesty
            pathSrc = pathSrc.replace("\\","/")

            f = open(pathSrc, "rb")                             #otvorim subor s "rb"
            data = f.read()
            f.close()
        else:
            print("error 2: incorrect input")
            continue

        fragments = splitIntoFragments(maxFragment, data)                                       #splitnutie spravy/suboru do fragmentov
        initPacket = createInitializationPacket(len(data), len(fragments), bytes(pathDest,encoding = "utf-8"))                  #vytvorenie inicializacneho packetu

        client_socket.sendto(initPacket, (ip, port))                        #poslem init packet
        print("posielam init packet: full dlzka dat: {}, pocet fragmentov: {}, pathDest: {}\nmax velkost fragmentu: {}".format(len(data), len(fragments), pathDest, maxFragment+32+headersize))
        if(len(fragments)==1):
            print("velkost packetu je {}".format(len(fragments[0])+32))
        if(choice == "subor"):
            print("meno suboru: {}".format(getFileName(pathSrc)))
        data, address = client_socket.recvfrom(1500)
        print("server vravi:")
        print(str(data))

        if(simChoice == "y"):
           if(errorFragIndex>=len(fragments)):          #ak bola zadana prilis vysoka hodnota pre index chybneho fragmentu, nastavi sa na posledny
               errorFragIndex = len(fragments) - 1
        i=0                                             #counter uspesne poslanych fragmentov(uspesne poslane su iba ak dojde spravny flag aj seq)
        while(True):                                    #v tomto loope posielam jednotlive fragmenty
            client_socket.settimeout(1.0)                   #timeout pre stop&wait ARQ
            if(simChoice == "y" and errorFragIndex == i and simError == 1):                     #odoslanie chybneho fragmentu
                temp = fragments[i]
                errorFragment = temp[:(len(temp)-1)]
                client_socket.sendto(errorFragment, (ip, port))
                simError = 0
            else:                                   #poslem fragment, cakam na odpoved
                client_socket.sendto(fragments[i], (ip, port))
                #ytemp = fragments[i]
                #ydata = ytemp[headersize:]
                #print("                                                                        data sent: {}".format(str(ydata)))

            try:                                                    #ak pride odpoved v dostatocny cas, s korektnym flagom(ACK) a sequence numberom, fragment prisiel spravne
                data, address = client_socket.recvfrom(1500)
                #print("preslo {} ms".format(timegoneby))
                flag, seq = getFlagAndSeqNum(data)
                #print("server response flag: {} seq: {}".format(flag,seq))
                if(flag == "ACK" and seq == (i+1) % 2):                         #spravny flag a seq number -> zvysim hodnotu i(counter spravnych fragmentov)
                    i+=1
                if(i == len(fragments)):                                        #ak som vsetky spravne poslal a spravne aj prisli, poslem posledny ukoncovaci packet
                    transferOver = bytes("transferover", encoding="utf-8")
                    client_socket.sendto(transferOver, (ip, port))
                    transferOverResponse, address = client_socket.recvfrom(1024)
                    if (transferOverResponse == bytes("transferoverindeed", encoding="utf-8")):
                        print("transfer successfully over\n")
                        break
            except socket.timeout:
                print('time out triggered!')

        print("chcete pokracovat v posielani? (y/n):")                      #vyber, ci chceme posielat dalsiu spravu/subor
        choiceYN = input()
        if (choiceYN != "y"):                                               #ak nechceme, posle sa packet, ktory ukonci server, a ukonci sa aj klient
            closingPacket = bytes("koniecnasejkomunikacieahoj",encoding="utf-8")
            client_socket.sendto(closingPacket, (ip, port))
            endresponse, address = client_socket.recvfrom(1024)
            if(endresponse == bytes("koniecnasejkomunikacieahoj",encoding="utf-8")):            #ak su koncove packety spravne prijate, mozeme ukoncit co sme chceli
                client_socket.close()
                print("klient ukonceny")
                break
        elif(choiceYN == "y"):
            continue


def mainloop():
    while(True):
        print("zadajte volbu (server/client): ")
        choice = input()
        print("zadajte IP: ")
        udpIP = input()
        print("zadajte PORT: ")
        udpPORT = int(input())
        if(choice == "server"):                         #zavolam funkciu, ktora ovlada server
            print("server:")
            serverSocket(udpIP, udpPORT)
        elif(choice == "client"):                       #zavolam funkciu, ktora ovlada klienta
            print("client:")
            clientSocket(udpIP, udpPORT)
        elif(choice == "koniec"):
            print("koniec programu")
            break


mainloop()                          #volam mainloop, ktory ovlada chod celeho programu

