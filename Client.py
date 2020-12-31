import socket
import struct
import time
import getch
import msvcrt


class client():
    buffersize=1024
    teamName="ATeam"
    UDPPort=13117

    def openSocketUDP(self):
        """
        this function open UDP socket for the client and recv the offers form the server
        """
        while(True):
            serverPort = self.UDPPort
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) 
            print ("Client started, listening for offer reqests...")
            rec=True
            clientSocket.bind(("",serverPort))
            while (rec==True): #search for offers - if offer is found stop searching
                data, addr = clientSocket.recvfrom(self.buffersize)
                unpacked = struct.unpack("Ibh",data)
                if (hex(unpacked[0])=='0xfeedbeef' and unpacked[1]==2): #check if the offer is in the format
                    rec=False #if so stop looking for offers
            print("Received offer from %s, attempting to connect..."%addr[0])
            self.openSocketTCP(unpacked[2],addr[0]) #open tcp connection 

    def openSocketTCP(self,port,IP):
        """
        this function open TCP socket for the client and try to connect the server 
        params: port- the port number of the connection
                IP- the IP number of the connection
        """
        try:
            serverName = IP
            serverPort = port
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort)) #connection to the TCP
            sentence = self.teamName.encode()
            clientSocket.send(sentence) #send to the sever my team name
            modifiedSentence = clientSocket.recv(self.buffersize)
            print (modifiedSentence.decode()) 
            timeout = time.time()+10
            while msvcrt.kbhit():#make sure that only the keys pressed in this 10 seconds are counted
                msvcrt.getch()
            while time.time()<=timeout: #the game is for 10 seconds
                if(msvcrt.kbhit()):
                    clientSocket.send(getch.getch())
            modifiedSentence = clientSocket.recv(self.buffersize)
            print (modifiedSentence.decode())
            print("Server disconnected, listening for offer requests...")
            clientSocket.close()
        except socket.error:
            print("Something wrong happen, try to re-connect")
            clientSocket.close()

        
if __name__ == "__main__":
    Client1=client()
    Client1.openSocketUDP()    