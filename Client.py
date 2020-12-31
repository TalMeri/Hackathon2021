import socket
import struct
import time
import getch
import msvcrt

class client():

    def openSocketUDP(self):
        """
        docstring
        """
        while(True):
            serverPort = 13117
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) 
            print ("Client started, listening for offer reqests...")
            rec=True
            clientSocket.bind(("",serverPort))
            while (rec==True):
                data, addr = clientSocket.recvfrom(1024)
                unpacked = struct.unpack("Ibh",data)
                if (hex(unpacked[0])=='0xfeedbeef' and unpacked[1]==2):
                    rec=False
                print("Received offer from %s, attempting to connect..."%addr[0])
                self.openSocketTCP(unpacked[2],addr[0])

    def openSocketTCP(self,port,IP):
        """
        docstring
        """
        try:
            serverName = IP
            serverPort = port
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))
            sentence = b"ATeam\n"
            clientSocket.send(sentence)
            modifiedSentence = clientSocket.recv(1024)
            print (modifiedSentence.decode())
            timeout = time.time()+10
            while time.time()<=timeout:
                if(msvcrt.kbhit()):
                    clientSocket.send(getch.getch())
            modifiedSentence = clientSocket.recv(1024)
            print (modifiedSentence.decode())
            print("Server disconnected, listening for offer requests...")
            clientSocket.close()
        except socket.error:
            print("Something wrong happen, try to re-connect")
            clientSocket.close()

        
if __name__ == "__main__":
    Client1=client()
    Client1.openSocketUDP()    