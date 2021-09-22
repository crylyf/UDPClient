
import sys
from os import * 
from socket import *
import io

def main(port): 
    ##create server socket
    serverPort = port 
    serverSocket =socket(AF_INET,SOCK_STREAM)
    serverSocket.bind (('',port))
    serverSocket.listen(1) 
    print ('The server is ready to receive') 
    
    while True: 
        connectionSocket, addr =serverSocket.accept()
        ##waiting for client input 
        sentence = connectionSocket.recv(1024).decode()
        if sentence == 'EXIT':
            serverSocket.close()
            exit()
    
        command = sentence.split()[0]
        file = sentence.split()[1]
        
        ##sending OK signal to client for stage 2 initiation
        connectionSocket.send("ok".encode())
        
        con2= connectionSocket.recv(1024).decode() 
    
        clientPort = int(con2.split()[0].replace(",",''))
        clientAddr = con2.split()[1]
        
        connectionSocket.close() 
        
        connectionSocket2=socket(AF_INET,SOCK_STREAM)
        connectionSocket2.connect((clientAddr,clientPort))
        
        if command == "GET": 
            ##send the file over to the new server 
            f =io.open(file,'rb')
    
            lines =f.readlines()
            
            for i in lines: 
                connectionSocket2.send(i)
                
        
            print('file send')
            f.close()
            connectionSocket2.close()
            exit()
        else: 
            ##action = put
            f=io.open("NEW_" + file,'wb')
        
            
            str3 = connectionSocket2.recv(1024)
            while (str3):
                f.write (str3)
                str3= connectionSocket2.recv(1024)
            print("file downloaded")
            f.close()
            connectionSocket2.close()
            exit()
        
        connectionSocket2.close() 
        
main(int(sys.argv[1]))


                
    
