from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    myChecksum = 0
    myID = os.getpid() & 0xFFFF 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)
  
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            timeLeft = TIMEOUT
            destAddr = gethostbyname(hostname)

            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
           
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []:
                    print(" %d   *      *     *   Request timed out." % ttl)
                    continue  # Continue trying the next TTL

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft -= howLongInSelect

                if timeLeft <= 0:
                    print(" * * * Request timed out.")
                    continue
            except timeout:
                continue
            else:
                icmpHeader = recvPacket[20:28]
                types, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

                if types == 11 or types == 3 or types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    rtt = (timeReceived - timeSent) * 1000

                    # Get the hostname corresponding to the IP address
                    try:
                        hostName = gethostbyaddr(addr[0])[0]
                    except herror:
                        hostName = addr[0]  # If we can't resolve, use IP address
                    
                    print(f" {ttl} rtt= {rtt:.0f}ms {hostName} ({addr[0]})\n")
                else:
                    print("error")
                break  
            finally:
                mySocket.close()

print("Alemanha")
get_route("84.200.69.80") 

print("Ásia - onde nao sei")
get_route("4.2.2.2") 

print("Oceania")
get_route("202.158.214.106")

print("África")
get_route("196.25.1.1")

# get_route("www.google.com")



