import socket
import time
import struct
import threading
import random

class server():
    Group1 = []
    Group2 = []
    sumGroup1=0
    sumGroup2=0
    timeout=0
    threads=[]
    
    def openSocketUDP(self):
        """
        docstring
        """
        serverPort = 13117
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) 
        clientSocket.settimeout(10)
        try:
            IP=socket.gethostbyname(socket.gethostname())
            print("Server started, listening on IP address %s"%IP)   
            while (True):
                message = struct.pack('Ibh',0xfeedbeef,0x2,0x67)
                clientSocket.sendto(message,('<broadcast>',serverPort))
                time.sleep(1)
        except socket.timeout():
            clientSocket.close()
        

    def openSocketTCP(self):
        serverPort = 103
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(("",serverPort))
        while (True):
            UDPThread=threading.Thread(target = server1.openSocketUDP, args = ())
            UDPThread.start()
            serverSocket.settimeout(10)
            serverSocket.listen(1)
            try:
                while (True):
                    connectionSocket, addr = serverSocket.accept()
                    sentence = connectionSocket.recv(1024)
                    choose=random.choice(["Group1","Group2"])
                    if (choose=="Group1"):
                        self.Group1.append(sentence)
                    else:
                        self.Group2.append(sentence)
                    self.threads.append(threading.Thread(target=self.game,args=(connectionSocket,addr,choose)))
            except socket.timeout:
                if (len(self.threads)>0):
                    for thread in self.threads:
                        thread.start()
                    for thread in self.threads:
                        thread.join()
                    self.threads=[]
                    print("Game over, sending out offer requests...")
                    self.Group1=[]
                    self.Group2=[]
                    self.sumGroup1=0
                    self.sumGroup2=0
                    
    def game(self,connectionSocket,addr,choose):
        try:
            MSG = "Welcome to Keyboard Spamming Battle Royale."+"\n"
            MSG+="Group 1:"+"\n""=="+"\n"
            for team in self.Group1:
                MSG+=str(team.decode())
            MSG+="\n"+"Group 2:"+"\n""=="+"\n"
            for team in self.Group2:
                MSG+=str(team.decode())
            MSG+="\nStart pressing keys on your keyboard as fast as you can!!"
            connectionSocket.send(str.encode(MSG))
            sum=0
            connectionSocket.settimeout(10)
            try:
                while (True):
                    sentence = connectionSocket.recv(1024)
                    print(sentence)
                    sum+=1
                    print(sum)
            except socket.timeout:
                if (choose=="Group1"):
                    self.sumGroup1+=sum
                else:
                    self.sumGroup2+=sum
                time.sleep(1)
                MSG="Game over!"
                MSG+="\n"+"Group 1 typed in "+str(self.sumGroup1)+" characters. Group 2 typed in "+str(self.sumGroup2)+" characters."
                if (self.sumGroup1>self.sumGroup2):
                    win = "Group 1"
                else:
                    win = "Group 2"
                MSG+="\n"+"%s wins!"%win
                MSG+="\n"+"\n"+"Congratulations to the winners:"+"\n"+"=="+"\n"
                if (win == "Group 1"):
                    for team in self.Group1:
                        MSG+=str(team.decode())
                else:
                    for team in self.Group2:
                        MSG+=str(team.decode())
                connectionSocket.send(str.encode(MSG))
                connectionSocket.close()
        except socket.error:
            print("Something wrong happen, try to re-connect")
            connectionSocket.close()


if __name__ == "__main__":

    server1 = server()
    server1.timeout = time.time()+10
    threading.Thread(target = server1.openSocketTCP, args = ()).start()
    

    