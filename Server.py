import socket
import time
import struct
import threading
import random

class server():
    Group1 = []
    Group2 = []
    threads = []
    sumGroup1=0
    sumGroup2=0

    
    def openSocketUDP(self):
        """
        this function open UDP socket for the server and sent broadcast messages
        send the massage every second for 10 seconds 
        """
        serverPort = 13117
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) 
        serverSocket.settimeout(10) #need to send the massages for 10 seconds
        try:
            IP=socket.gethostbyname(socket.gethostname())
            print("Server started, listening on IP address %s"%IP)   
            while (True):
                message = struct.pack('Ibh',0xfeedbeef,0x2,0x837)#packet format port 2103 
                serverSocket.sendto(message,('<broadcast>',serverPort))
                time.sleep(1)
        except socket.timeout():
            serverSocket.close()
        

    def openSocketTCP(self):
        """
        this function open TCP socket for the server and open threads for each user in the game
        after 10 seconds start the games for the players
        """
        serverPort = 2103
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(("",serverPort))
        while (True):
            UDPThread=threading.Thread(target = server1.openSocketUDP, args = ())
            UDPThread.start()
            serverSocket.settimeout(10) #the connection part need to take 10 seconds
            serverSocket.listen(1) 
            try:
                while (True):
                    connectionSocket, addr = serverSocket.accept()
                    sentence = connectionSocket.recv(1024)
                    choose=random.choice(["Group1","Group2"]) #choose Group randomly 
                    if (choose=="Group1"):
                        self.Group1.append(sentence)
                    else:
                        self.Group2.append(sentence)
                    self.threads.append(threading.Thread(target=self.game,args=(connectionSocket,choose)))
            except socket.timeout: #after 10 seconds open the games for the players
                if (len(self.threads)>0):
                    for thread in self.threads:
                        thread.start()
                    for thread in self.threads:
                        thread.join()
                    #after the games is over set up the elements for the next game
                    self.threads=[] 
                    print("Game over, sending out offer requests...")
                    self.Group1=[]
                    self.Group2=[]
                    self.sumGroup1=0
                    self.sumGroup2=0
                    
    def game(self,connectionSocket,choose):
        """
        this function is the game of the server count how much keys each group has prassed 
        params: connectionSocket- the socket of each connection with user and the server
                choose - the group of the player
        """
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
            connectionSocket.settimeout(10) #the game is only 10 seconds
            try:
                while (True):
                    connectionSocket.recv(1024)
                    sum+=1 #add 1 to the sum when key is prassed 
            except socket.timeout: #print the scores 
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
                connectionSocket.send(str.encode(MSG)) #send the scores to the players
                connectionSocket.close()
        except socket.error: 
            print("Something wrong happen, try to re-connect")
            connectionSocket.close()


if __name__ == "__main__":

    server1 = server()
    threading.Thread(target = server1.openSocketTCP, args = ()).start()
    

    