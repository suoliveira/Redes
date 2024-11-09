from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8

def rtts(rtt):
    avg = sum(rtt) / len(rtt)
    max_rtt = max(rtt)
    min_rtt = min(rtt)
    return avg, max_rtt, min_rtt

rtt_list = []
countPings = 0

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

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        
        if packetID == ID:  # Check if the packet ID matches
            # Calculate round-trip time (RTT)
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            rtt = (timeReceived - timeSent) * 1000  # Convert to ms
            return rtt
       
        
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header
    myChecksum = checksum(header + data)
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff

    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    global countPings
    dest = gethostbyname(host)
    print("")
    
    global rtt_list
    packets_sent = 0
    packets_received = 0

    for i in range(0,2):
        delay = doOnePing(dest, timeout)
        packets_sent += 1
        if delay != "Request timed out.":
            packets_received += 1
            countPings += 1
            rtt_list.append(delay)
            print(f"pingando para {dest}: tempo= {delay:.2f} ms")
        else:
            print(delay)
        time.sleep(1)
    
    # Calculate packet loss
    packet_loss = ((packets_sent - packets_received) / packets_sent) * 100
    print(f"\n{packets_sent} enviados, {packets_received} recebidos, {packet_loss:.1f}% perdidos\n")
    

ping("127.0.0.1") 

print("BR")
ping("186.192.252.1") 
ping("nic.br") 

print("Ásia - onde nao sei")
ping("4.2.2.2") 

print("Oceania")
ping("202.158.214.106")

print("África")
ping("196.25.1.1")

print("Alemanha")
ping("84.200.69.80")

avg_rtt, max_rtt, min_rtt = rtts(rtt_list)
print("\n********** Estatísticas **********")
print(f"RTT mínimo: {min_rtt:.2f} ms")
print(f"RTT máximo: {max_rtt:.2f} ms")
print(f"RTT médio: {avg_rtt:.2f} ms")






