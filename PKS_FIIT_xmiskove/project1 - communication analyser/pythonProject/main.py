from scapy.compat import bytes_hex
from scapy.all import rdpcap

class tcpkom:
    __slots__ = ("packetnum", "packetflags", "sip", "dip", "sport", "dport", "handshake", "end", "protocol")

    def __init__(self, sip, dip, sport, dport):
        self.handshake = "no"
        self.end = "no"
        self.packetnum = []
        self.packetflags = []
        self.sport = sport
        self.dport = dport
        self.sip = sip
        self.dip = dip
        self.protocol = "empty"
class arpkom:
    __slots__ = ("packetnum", "sip", "dip", "open")

    def __init__(self, sip, dip):
        self.open = "yes"
        self.packetnum = []
        self.sip = sip
        self.dip = dip
class tftpkom:
    __slots__ = ("packetnum")

    def __init__(self):
        self.packetnum = []

print("Zadajte meno programu, ktorý chcete otvoriť(aj so suffixom):")
subor = input()
openedPackets = rdpcap('vzorky_pcap_na_analyzu/'+subor)

def getFrameLengthAPI(pkt):                     #vrati dlzku ramca
    return int((len(pkt)-3)/2)
def getFrameLengthMedium(pkt):
    if((len(pkt)-3)/2<=60):
        return 64
    else:
        return int(4+(len(pkt)-3)/2)
def getDestMAC(strpkt):                     #funkcie vracaju MAC adresy
    return strpkt[2:14]
def getSrcMAC(strpkt):
    return strpkt[14:26]
def getSrcIP(strpkt,start):   #strpkt[54:62]                                funkcie zistuju IP adresy
    ip = ""
    for i in range(0, 4):
        ip += str(hexToDec(strpkt[(start+(i*2)):(start+2+(i*2))]))
        if i < 3:
            ip += "."
    return ip
def getDestIP(strpkt,start):   #strpkt[62:70]
    ip = ""
    for i in range(0, 4):
        ip += str(hexToDec(strpkt[(start+(i*2)):(start+2+(i*2))]))
        if i < 3:
            ip += "."
    return ip
def printMACAddresses(dest,src):                            #specificky formatovany print zo zadania
    if(len(dest)!=len(src)):
        return "error1"
    print("Zdrojová MAC adresa: ",end="")
    for x in range(0,len(src), 2):
        print("{}{} ".format(src[x], src[x + 1]), end="")
    print("")
    print("Cieľová MAC adresa: ", end="")
    for x in range(0, len(dest), 2):
        print("{}{} ".format(dest[x], dest[x + 1]), end="")
    print("")
def printIPv4Addresses(src,dest):
    print("zdrojová IP adresa: {}".format(src))
    print("cieľová IP adresa: {}".format(dest))
def printFrameLengths(first,second):
    print("dĺžka rámca poskytnutá pcap API – {} B".format(first))
    print("dĺžka rámca prenášaného po médiu – {} B".format(second))
def printIPCount(listIP):                                       #vypis statistiky IPv4 komunikacie
    if(len(listIP)==0):
        print("Nenašli sa žiadne IPv4 pakety!")
        return
    print("IP adresy vysielajúcich uzlov:")
    max=0
    idx = 0
    for i in range(0,len(listIP)):
        if(max<listIP[i][1]):
            max=listIP[i][1]
            idx=i
        print(listIP[i][0])
    print("\nAdresa uzla s najväčším počtom odoslaných paketov:\n{}       {} paketov\n\n".format(listIP[idx][0],listIP[idx][1]))
def printBytes(strpkt):                                 #pozadovany vypis paketu na konci jeho analyzy
    n = 0
    for x in range(0, len(strpkt)):
        if(x==0 or x==1 or x==len(strpkt)-1):
            continue
        else:
            n += 1
            print(strpkt[x], end="")
            if(n%32 == 0):
                print("")
            elif(n%16 == 0):
                print("  ",end="")
            elif(n%2 == 0):
                print(" ", end="")
    print("\n")
def htdChar(c):#assuming its hexadec            #prevod pismeniek na cisla 16->10
    if c.isalpha() and len(c) == 1:
        if c.isupper():
            return int((ord(c)) - 55)
        else:
            return int((ord(c)) - 87)
    elif len(c) == 1:
        return int(c)
def hexToDec(str):                          #prevod hexadec do dec ked potrebujem ziskat konkretne cislo
    num = 0
    for i in range(len(str)-1,0-1,-1):
        num += int(htdChar(str[i])*(16**(1-i)))
    return num
def checkDIP(listIP, SIP):                  # zisti z listu IP adries ci treba pridavat novu alebo sa opakuje a iba zvysim hodnotu odoslanych paketov a vybavi to
    for i in range(0,len(listIP)):
        if(SIP == listIP[i][0]):
            listIP[i][1]+=1
            return
    listIP.append([SIP,1])
def getProtocol(n, typeStr):                            #prehlada subor pre ethertypy a SAPy
    if(typeStr == "Ethernet II"):
        nestedProtocol = findInTxt("#ETHERTYPE\n",n)
        return nestedProtocol
    elif(typeStr == "IEEE 802.3 LLC"):
        nestedProtocol = findInTxt("#SAP\n",n)
        return nestedProtocol
def analyzeFrame(strpkt,dmac,smac, listIP, tftpport, tftpNum, listArpRequests, packetNum, stage, listFilter, listTCP, listTFTP, listICMP):#26:30
    tftpportstart = tftpport
    decimalDecider = hexToDec(strpkt[26:28])*256 + hexToDec(strpkt[28:30])
    if decimalDecider > 1500:                                                               #cast pre Ethernet II
        frameType = "Ethernet II"
        print(frameType)                                                #print typu ramca
        printMACAddresses(dmac, smac)                                   #print MAC adries
        first_nested_protocol = getProtocol(decimalDecider, frameType)
        print(first_nested_protocol)                                    #print vnoreneho protokolu
        if(first_nested_protocol == "IPv4"):                                                            #cast pre IPv4
            SIP, DIP, second_nested_protocol, nextHeaderIndex = runIPv4(strpkt)
            checkDIP(listIP,SIP)
            printIPv4Addresses(SIP, DIP)                                #print IP adries
            print(second_nested_protocol)                               #print vnoreneho protokolu
            if(second_nested_protocol == "TCP"):                                                                #IPv4->TCP
                tcpPort = runTCP(strpkt, nextHeaderIndex, packetNum, listTCP, stage, DIP, SIP)
                if (tcpPort == "http" or tcpPort == "https ssl" or tcpPort == "telnet" or tcpPort == "ssh" or tcpPort == "ftp-data" or tcpPort == "ftp-control"):
                    listFilter[packetNum-1] = tcpPort
            elif(second_nested_protocol == "UDP"):                                                              #IPv4->UDP
                udpPort, tftpport = runUDP(strpkt, nextHeaderIndex, tftpport)
                if(tftpport != tftpportstart):
                    tftpNum+=1
                    if(stage==1):
                        newTFTPComm = tftpkom()
                        listTFTP.append(newTFTPComm)
                if(udpPort == "tftp"):
                    if(stage == 1):
                        listTFTP[tftpNum-1].packetnum.append(packetNum)
                    print("Číslo tftp komunikácie: {}".format(tftpNum))
                    listFilter[packetNum - 1] = udpPort
            elif(second_nested_protocol == "ICMP"):                                                             #IPv4->ICMP
                listFilter[packetNum - 1] = second_nested_protocol
                ICMPtype, ICMPname = runICMP(strpkt,nextHeaderIndex)
                print("ICMP type: {}".format(ICMPtype))
                if(stage == 1):
                    temp = 0
                    for k in range(0,len(listICMP)):
                        if((DIP == listICMP[k].dip and SIP == listICMP[k].sip) or (DIP == listICMP[k].sip and SIP == listICMP[k].dip)):
                            listICMP[k].packetnum.append(packetNum)
                            temp=1
                    if(temp == 0):
                        comm = arpkom(SIP,DIP)
                        comm.packetnum.append(packetNum)
                        listICMP.append(comm)
                if(ICMPname != "NotFound"):
                    print("ICMP name: {}".format(ICMPname))
        if(first_nested_protocol == "ARP"):                                                     #cast pre ARP
            runARP(strpkt, listArpRequests, packetNum, stage)
    else:                                                                                   #cast pre IEEE
        frameType = "IEEE 802.3"
        ieeeDecider = hexToDec(strpkt[30:32])
        if(ieeeDecider == 255):
            frameType+= " raw IPX"                                                      #raw->IPX (podla prednasky)
            print(frameType)                                            #print typu ramca
            printMACAddresses(dmac, smac)                               #print MAC adries
        elif(ieeeDecider == 170):                                                          #SNAP->koniec (podla cvicenia)
            frameType+= " LLC SNAP"
            print(frameType)                                            #print typu ramca
            printMACAddresses(dmac, smac)                               #print MAC adries
        else:
            frameType+= " LLC"
            print(frameType)                                            #print typu ramca
            printMACAddresses(dmac, smac)                               #print MAC adries
            first_nested_protocol = getProtocol(ieeeDecider, frameType)     #najde dalsi protokol
            print(first_nested_protocol)                                #print vnoreneho protokolu
            # print(first_nested_protocol)


    return tftpport, tftpNum
def findInTxt(categoryStr, num):                        #funkcia hlada string v subore a vrati priradeny protokol
    f = open('externysubor.txt', "r")
    numStr = str(num)
    numStr += "\n"
    for i in range(0, 1000):
        if (f.readline() == categoryStr):
            for y in range(0, 1000):
                cmp = f.readline()
                if (cmp == "EXIT" or cmp[0] == "#"):
                    #print("-----------------protocol not found!!!----------------------")
                    f.close()
                    return "NotFound"
                if (cmp == numStr):
                    nestedProtocol = f.readline().replace("\n", "")
                    #print("found!!!!!!!!!!!")
                    #print(nestedProtocol)
                    f.close()
                    return nestedProtocol
def findInTxtICMP(categoryStr, num):                        #funkcia hlada string v subore a vrati priradeny protokol
    f = open('ICMPsubor.txt', "r")
    numStr = str(num)
    numStr += "\n"
    for i in range(0, 1000):
        if (f.readline() == categoryStr):
            for y in range(0, 1000):
                cmp = f.readline()
                if (cmp == "EXIT" or cmp[0] == "#"):
                    #print("-----------------protocol not found!!!----------------------")
                    f.close()
                    return "NotFound"
                if (cmp == numStr):
                    nestedProtocol = f.readline().replace("\n", "")
                    #print("found!!!!!!!!!!!")
                    #print(nestedProtocol)
                    f.close()
                    return nestedProtocol
def runIPv4(strpkt):
    ihl = (htdChar(strpkt[31]))*4           #internet header length
    protocolNum = hexToDec(strpkt[48:50])
    IPv4NestedProtocol = findInTxt("#IPv4\n",protocolNum)
    SIP = getSrcIP(strpkt, 54)
    DIP = getDestIP(strpkt, 62)
    nextHeaderIndex = 30+(ihl*2) #tu zacina dalsi header
    return SIP, DIP, IPv4NestedProtocol, nextHeaderIndex
def runTCP(strpkt, startIndex, packetNum, listTCP, stage, dip, sip):
    SPortNum = (hexToDec(strpkt[startIndex:startIndex + 2]) * 256) + hexToDec(strpkt[startIndex + 2:startIndex + 4])
    DPortNum = (hexToDec(strpkt[startIndex+4:startIndex + 6]) * 256) + hexToDec(strpkt[startIndex + 6:startIndex + 8])
    SPort = findInTxt("#TCP\n", SPortNum)
    DPort = findInTxt("#TCP\n", DPortNum)
    realPort = 0
    if (SPort == "NotFound" and DPort != "NotFound"):
        print(DPort)
        realPort = DPort
    elif(SPort != "NotFound" and DPort == "NotFound"):
        print(SPort)
        realPort = SPort
    elif (SPort != "NotFound" and DPort != "NotFound" and DPort == SPort):
        print(DPort)
        realPort = DPort
    print("zdrojový port: {}".format(SPortNum))
    print("cieľový port: {}".format(DPortNum))
    if(stage == 1):
        TCPflag = findTCPFlag(strpkt, startIndex + 26)
        checkTCPcomm(packetNum, dip, sip, DPortNum, SPortNum, listTCP, TCPflag, realPort)
    return realPort
def findTCPFlag(strpkt, start):
    x = hexToDec(strpkt[start:start+2])
    flagStr = ""
    i = 128
    while True:                             #prevedie potrebne byty z hexadec do dec sustavy a z nej do 8-miestneho stringu binarnej formy, pretoze sa mi s tym v tomto pripade lepsie pracuje
        if(x>=i):                           # bin() funkcia vytvara binarne cislo s co najmensim poctom miest, co mi nevyhovuje
            x= x-i
            flagStr+="1"
        else:
            flagStr+="0"
        if(i>1):
            i= i/2
        else:
            break
    realFlag = ""
    if (flagStr[7] == "1"):
        realFlag += "FIN"
    if (flagStr[6] == "1"):
        realFlag += "SYN"
    if (flagStr[5] == "1"):
        realFlag += "RST"
    if (flagStr[4] == "1"):
        realFlag += "PUSH"
    if (flagStr[3] == "1"):
        realFlag += "ACK"
    return realFlag
def checkTCPcomm(packetNum, dip, sip, dport, sport, listTCP, TCPflag, TCPprotocol):
    if (TCPflag == "FINPUSHACK"):           #odstranenie (pre mna) nepotrebnych casti TCP komunikacnych flagov
        TCPflag = "FINACK"
    if (TCPflag == "RSTACK"):
        TCPflag = "RST"
    for i in range(0,len(listTCP)):                                                         #prehlada list TCP komunikacii a najde mozny threeway handshake
        if (listTCP[i].dip == dip and listTCP[i].sip == sip and listTCP[i].dport == dport and listTCP[i].sport == sport and listTCP[i].handshake == "no" and listTCP[i].end == "no"):#tieto podmienky zabezpecuju spravne poradie flagov v handshaku, checkuju porty, ipcky, flagy atd
            if(TCPflag == "ACK" and len(listTCP[i].packetnum) == 2 and listTCP[i].packetflags[0] == "SYN" and listTCP[i].packetflags[1] == "SYNACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
                listTCP[i].handshake = "yes"
                return
        if (listTCP[i].dip == sip and listTCP[i].sip == dip and listTCP[i].dport == sport and listTCP[i].sport == dport and listTCP[i].handshake == "no" and listTCP[i].end == "no"):
            if (TCPflag == "SYNACK" and len(listTCP[i].packetnum) == 1 and listTCP[i].packetflags[0] == "SYN"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
                return
            #kontrola data streamu v komunikacii, a RST ukoncenia komunikacie
        if (((listTCP[i].dip == dip and listTCP[i].sip == sip and listTCP[i].dport == dport and listTCP[i].sport == sport) or (listTCP[i].dip == sip and listTCP[i].sip == dip and listTCP[i].dport == sport and listTCP[i].sport == dport)) and (listTCP[i].handshake == "yes")):       #outgoing and incoming comm
            if (TCPflag == "PUSHACK" or TCPflag == "ACK" and listTCP[i].end == "no" and listTCP[i].packetflags[-1] != "FINACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if (TCPflag == "ACK" and listTCP[i].packetflags[-1] == "RST" and listTCP[i].end == "yes"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if (TCPflag == "RST" and listTCP[i].end == "no"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
                listTCP[i].end = "yes"

            #kontrola FINACK,ACK,FINACK,ACK ukoncenia
        if (listTCP[i].dip == sip and listTCP[i].sip == dip and listTCP[i].dport == sport and listTCP[i].sport == dport and listTCP[i].handshake == "yes" and listTCP[i].end == "no"):
            if(TCPflag == "FINACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if (TCPflag == "ACK" and listTCP[i].packetflags[-1] == "FINACK" and listTCP[i].packetflags[-2] == "ACK" and listTCP[i].packetflags[-3] == "FINACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
                listTCP[i].end = "yes"
        if (listTCP[i].dip == dip and listTCP[i].sip == sip and listTCP[i].dport == dport and listTCP[i].sport == sport and listTCP[i].handshake == "yes" and listTCP[i].end == "no"):
            if (TCPflag == "FINACK" and listTCP[i].packetflags[-1] == "ACK" and listTCP[i].packetflags[-2] == "FINACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if (TCPflag == "ACK" and listTCP[i].packetflags[-1] == "FINACK"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)


            #kontrola FIN,ACK,FIN,ACK komunikacie
        if (listTCP[i].dip == sip and listTCP[i].sip == dip and listTCP[i].dport == sport and listTCP[i].sport == dport and listTCP[i].handshake == "yes" and listTCP[i].end == "no"):
            if(TCPflag == "FIN"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if(TCPflag == "ACK" and listTCP[i].packetflags[-1] == "FIN" and listTCP[i].packetflags[-2] == "ACK" and listTCP[i].packetflags[-3] == "FIN"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
                listTCP[i].end = "yes"
        if (listTCP[i].dip == dip and listTCP[i].sip == sip and listTCP[i].dport == dport and listTCP[i].sport == sport and listTCP[i].handshake == "yes" and listTCP[i].end == "no"):
            if (TCPflag == "FIN" and listTCP[i].packetflags[-1] == "ACK" and listTCP[i].packetflags[-2] == "FIN"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)
            if (TCPflag == "ACK" and listTCP[i].packetflags[-1] == "FIN"):
                listTCP[i].packetflags.append(TCPflag)
                listTCP[i].packetnum.append(packetNum)


    if (TCPflag == "SYN"):      #vytvori novu komunikaciu
        newComm = tcpkom(sip,dip,sport,dport)
        newComm.packetnum.append(packetNum)
        newComm.packetflags.append(TCPflag)
        newComm.protocol = TCPprotocol
        listTCP.append(newComm)
def runUDP(strpkt, startIndex, tftpport):
    SPortNum = (hexToDec(strpkt[startIndex:startIndex + 2]) * 256) + hexToDec(strpkt[startIndex + 2:startIndex + 4])
    DPortNum = (hexToDec(strpkt[startIndex + 4:startIndex + 6]) * 256) + hexToDec(strpkt[startIndex + 6:startIndex + 8])
    SPort = findInTxt("#UDP\n", SPortNum)
    DPort = findInTxt("#UDP\n", DPortNum)
    realPort = 0
    checktftp, tftpport = findTFTP(SPortNum, DPortNum,tftpport)
    if(checktftp == "yestftp"):                                     #ak najdem tftp port tak sa to musi handlovat jednotlivo a inak od ostatnych portov
        realPort = "tftp"
        print(realPort)
        print("zdrojový port: {}".format(SPortNum))
        print("cieľový port: {}".format(DPortNum))
        return realPort, tftpport
    if (SPort == "NotFound" and DPort != "NotFound"):
        print(DPort)
        realPort = DPort
    elif(SPort != "NotFound" and DPort == "NotFound"):
        print(SPort)
        realPort = SPort
    elif (SPort != "NotFound" and DPort != "NotFound" and DPort == SPort):
        print(DPort)
        realPort = DPort
    print("zdrojový port: {}".format(SPortNum))
    print("cieľový port: {}".format(DPortNum))
    return realPort, tftpport
def runICMP(strpkt, startIndex):
    typeNum = hexToDec(strpkt[startIndex:startIndex+2])
    nameNum = hexToDec(strpkt[startIndex+2:startIndex+4])
    type = findInTxtICMP("#TYPE\n",typeNum)
    if(typeNum == 3):
        name = findInTxtICMP("#NAME3\n", nameNum)
    elif(typeNum == 5):
        name = findInTxtICMP("#NAME5\n", nameNum)
    elif (typeNum == 11):
        name = findInTxtICMP("#NAME11\n", nameNum)
    elif (typeNum == 12):
        name = findInTxtICMP("#NAME12\n", nameNum)
    else:
        name = "NotFound"
    return type, name
def runARP(strpkt, listArpRequests, packetNum, stage):
    opNum = (hexToDec(strpkt[42:44])*256)+(hexToDec(strpkt[44:46]))
    if opNum == 1 :
        operationName = "Request"
    elif opNum == 2:
        operationName = "Reply"
    else:
        operationName = "opname error"
    srcHardwareAddress = strpkt[46:58]
    srcProtocolAddress = getSrcIP(strpkt, 58)
    destHardwareAddress = strpkt[66:78]
    destProtocolAddress = getDestIP(strpkt, 78)
    printMACAddresses(destHardwareAddress,srcHardwareAddress)
    printIPv4Addresses(srcProtocolAddress, destProtocolAddress)
    print(operationName)
    if(stage == 1):
        groupARPup(operationName, destProtocolAddress, srcProtocolAddress, packetNum, listArpRequests)
def groupARPup(operation, dip, sip, packetNum, listArp):
    #print("dip: {} sip: {}")
    for i in range(0,len(listArp)):
        if(listArp[i].sip == sip and listArp[i].dip == dip and operation == "Request" and listArp[i].open=="yes"):
            listArp[i].packetnum.append(packetNum)
            return
        elif(listArp[i].sip == dip and listArp[i].dip == sip and operation == "Reply" and listArp[i].open=="yes"):
            listArp[i].packetnum.append(packetNum)
            listArp[i].open = "no"
            return
    newCommHaha = arpkom(sip, dip)
    newCommHaha.packetnum.append(packetNum)
    if(operation == "Reply"):
        newCommHaha.open = "brick"
    listArp.append(newCommHaha)
def findTFTP(port1, port2, tftpport):
    if(port1 == 69 or port2 == 69):
        if(port1!=69):
            tftpport = port1
            return "yestftp", tftpport
        if(port2!=69):
            tftpport = port2
            return "yestftp", tftpport
    else:
        if((port1 == tftpport or port2 == tftpport) and tftpport!=-1):
            return "yestftp", tftpport
        else:
            return "notftp", tftpport
def onePacketLoop(packets, n, listIP, tftpport, tftpNum, listArpRequests, stage, listFilter, listTCP, listTFTP, listICMP):          #riesenie jedneho paketu
    if (len(openedPackets) < n) or n <= 0:
        print("Packet not found")
        return
    one_packet = bytes_hex(packets[n-1])
    strpacket = str(one_packet)
    frameLengthAPI = getFrameLengthAPI(strpacket)
    frameLengthMedium = getFrameLengthMedium(strpacket)
    dest_mac = getDestMAC(strpacket)
    src_mac = getSrcMAC(strpacket)
    print("rámec {}".format(n))
    printFrameLengths(frameLengthAPI,frameLengthMedium)
    tftpport, tftpNum = analyzeFrame(strpacket, dest_mac, src_mac, listIP, tftpport, tftpNum, listArpRequests, n, stage, listFilter, listTCP, listTFTP, listICMP)

    printBytes(strpacket)
    return tftpport, tftpNum
def fullLoop(start, finish):                            #funkcia ktora sa stara o spravne fungovanie programu
    listFilter = []
    for x in range(start, finish+1):
        listFilter.append("empty")
    listIP = []
    tftpport = -1
    tftpNum = 0
    listArpRequests = []
    listICMP = []
    listTCP = []
    listTFTP = []
    for i in range(start, finish+1):
        tftpport, tftpNum = onePacketLoop(openedPackets, i, listIP, tftpport, tftpNum, listArpRequests, 1, listFilter, listTCP, listTFTP, listICMP)
    printIPCount(listIP)

    print("Zadajte meno protokolu z úlohy 4 (\"http\", \"https ssl\", \"telnet\", \"ssh\", \"ftp-data\", \"ftp-control\", \"tftp\", \"ICMP\", \"ARP\"):")
    inputStr = input()
    filterPrint(listFilter, listArpRequests, listTCP, listTFTP, inputStr, listICMP)
    #specificPrint("ICMP", listFilter)
    #ARPLoop(listArpRequests)
    #for fx in range(0,len(listTCP)):
    #    print("komunikacia c. {}".format(fx + 1))
    #    for fy in range(len(listTCP[fx].packetnum)):
    #        print(listTCP[fx].packetnum[fy])
def filterPrint(listFilter, listARP, listTCP, listTFTP, inputStr, listICMP):                #specificke vypisy pre specificke poziadavky
    count = 0
    if(inputStr == "tftp" or inputStr == "ICMP"):
        specificPrint(inputStr, listFilter, listTFTP, listICMP)
    elif(inputStr == "ARP"):
        ARPLoop(listARP)
    elif(inputStr == "http" or inputStr == "https ssl" or inputStr == "telnet" or inputStr=="ssh" or inputStr == "ftp-data" or inputStr == "ftp-control"):
        listarpfake = []
        listIP = []
        tftpport = -1
        tftpNum = 0
        completeCount = 0
        incompleteCount = 0
        for fx in range(0,len(listTCP)):
            if(listTCP[fx].protocol == inputStr and listTCP[fx].handshake == "yes" and completeCount==0 and listTCP[fx].end == "yes"):
                count+=1
                completeCount+=1
                print("{} kompletna komunikacia c. {}".format(inputStr, count))
                if(len(listTCP[fx].packetnum)<=20):
                    for fy in range(0,len(listTCP[fx].packetnum)):
                        #print(listTCP[fx].packetnum[fy])
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
                elif(len(listTCP[fx].packetnum)>20):
                    for fy in range(0,10):
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
                    for fy in range(len(listTCP[fx].packetnum)-10, len(listTCP[fx].packetnum)):
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
            if (listTCP[fx].protocol == inputStr and listTCP[fx].handshake == "yes" and incompleteCount==0 and listTCP[fx].end == "no"):
                count += 1
                incompleteCount+=1
                print("{} nekompletna komunikacia c. {}".format(inputStr, count))
                if (len(listTCP[fx].packetnum) <= 20):
                    for fy in range(0, len(listTCP[fx].packetnum)):
                        # print(listTCP[fx].packetnum[fy])
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
                elif (len(listTCP[fx].packetnum) > 20):
                    for fy in range(0, 10):
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
                    for fy in range(len(listTCP[fx].packetnum) - 10, len(listTCP[fx].packetnum)):
                        tftpport, tftpNum = onePacketLoop(openedPackets, listTCP[fx].packetnum[fy], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listTCP, listarpfake, listarpfake)
def breakARP(listARP):                                                              #rozdeli pakety neuplnej komunikacie do samostatnych komunikacii po jednom ako sa pise v zadani
    iter = len(listARP)
    for x in range(0,iter):
        iterxxxxx = len(listARP[x].packetnum)
        for y in range(0,iterxxxxx):
            if(listARP[x].open == "yes" and len(listARP[x].packetnum)>1):               #ak je komunikacia bez reply a ma viac ako 1 paket
                poppedpaketnum = listARP[x].packetnum.pop(len(listARP[x].packetnum)-1)  #odstranim posledny paket a dam ho do novovytvorenej komunikacie
                newCommHaha = arpkom(0, 0)
                newCommHaha.packetnum.append(poppedpaketnum)
                listARP.append(newCommHaha)
def ARPLoop(listARP):                #specificke vypisy pre specificke poziadavky
    listIP= []
    listx = []
    tftpport = -1
    tftpNum = 0
    listArpRequests = []
    comNum = 0
    for x in range(0,len(listARP)):
        if(listARP[x].open == "no"):
            comNum+=1
            print("ARP komunikácia číslo {}: \n".format(comNum))
            if len(listARP[x].packetnum) <= 20:
                for y in range(0,len(listARP[x].packetnum)):
                    onePacketLoop(openedPackets, listARP[x].packetnum[y], listIP, tftpport, tftpNum, listArpRequests, 2, listx, listx, listx, listx)
            else:
                for y in range(0,10):
                    onePacketLoop(openedPackets, listARP[x].packetnum[y], listIP, tftpport, tftpNum, listArpRequests, 2, listx, listx, listx, listx)
                for y in range(len(listARP[x].packetnum)-10,len(listARP[x].packetnum)):
                    onePacketLoop(openedPackets, listARP[x].packetnum[y], listIP, tftpport, tftpNum, listArpRequests, 2, listx, listx, listx, listx)
    print("Nekompletná ARP komunikácia:")
    for x in range(0,len(listARP)):
        if(listARP[x].open != "no"):
            for y in range(0,len(listARP[x].packetnum)):
                onePacketLoop(openedPackets, listARP[x].packetnum[y], listIP, tftpport, tftpNum, listArpRequests, 2, listx, listx, listx, listx)
def specificPrint(filter, listFilter, listTFTP, listICMP):                #specificke vypisy pre specificke poziadavky
    #print("\nVýpis všetkých {} paketov\n".format(filter))
    listarpfake = []
    listIP = []
    tftpport = -1
    tftpNum = 0
    if(filter == "ICMP"):
        for x in range(0,len(listICMP)):
            print("ICMP komunikácia číslo: {}".format(x+1))
            if (len(listICMP[x].packetnum) <= 20):
                for y in range(0, len(listICMP[x].packetnum)):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listICMP[x].packetnum[y], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
            elif (len(listICMP[x].packetnum) > 20):
                for y in range(0, 10):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listICMP[x].packetnum[y], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
                for y in range(len(listICMP[x].packetnum)-10,len(listICMP[x].packetnum)):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listICMP[x].packetnum[y], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
    elif(filter == "tftp"):
        for i in range(0,len(listTFTP)):
            if(len(listTFTP[i].packetnum) <= 20):
                for fx in range(0,len(listTFTP[i].packetnum)):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listTFTP[i].packetnum[fx], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
            elif(len(listTFTP[i].packetnum) > 20):
                for fx in range(0,10):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listTFTP[i].packetnum[fx], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
                for fx in range(len(listTFTP[i].packetnum)-10,len(listTFTP[i].packetnum)):
                    tftpport, tftpNum = onePacketLoop(openedPackets, listTFTP[i].packetnum[fx], listIP, tftpport, tftpNum, listarpfake, 2, listFilter, listarpfake, listarpfake, listarpfake)
fullLoop(1, len(openedPackets))   #zaciatok programu, volanie potrebnej funkcie
