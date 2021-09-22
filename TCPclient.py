#!/usr/bin/python3
import sys
from os import * 
from socket import *
import os
import io


def main(name,port): 
    clientSocket=socket(AF_INET,SOCK_STREAM) 
    clientSocket.connect((name,port))
    
    str1 = input("Command and filename:")
    if str1 == 'EXIT':
        clientSocket.send(str1.encode())
        clientSocket.close 
        exit()
    ##get the command and filename
    command = str1.split()[0]
    file = str1.split()[1]
    ##send the command and file name to the server
    clientSocket.send(str1.encode())
    
    ##waiting for the OK signal 
    signal = clientSocket.recv(1024).decode()

    ##proceed to phase 2 the data exchange
    if signal == "ok":
        print(signal)
        connectionSocket2=socket(AF_INET,SOCK_STREAM)
        ##port 0 = any free port 
        connectionSocket2.bind(('',0))
        ##get the port and server name of the new connection 
        new_port = connectionSocket2.getsockname()[1]
        new_name = gethostname()

        list1 = [str(new_port) +', ', new_name]
        str1 = ''.join(list1)
        connectionSocket2.listen(1)
        ##send the new port and server name to the server 
        clientSocket.send(str1.encode())
        clientSocket.close() 

        connectionSocket2,addr= connectionSocket2.accept() 
        
        if command == 'GET':
    
            buffer = io.DEFAULT_BUFFER_SIZE
        
            f= io.open('NEW_' + file , 'wb')
        
            
            str3= connectionSocket2.recv(1024)
        
            while str3: 
                f.write (str3) 
                str3 = connectionSocket2.recv(1024)
            
            f.close
            print('file succesfully downloaded')
            
        else: 
            ##command == PUT 
        
            f=io.open(file,'rb')
            lines = f.readlines()
        
            for i in lines: 
                connectionSocket2.send(i)
            f.close()
            print('file succesfully sent')
            connectionSocket2.close()
            exit() 
             
        
        connectionSocket2.close() 
    else: 
        ##close the socket, nothing happens
        clientSocket.close() 
        
main(sys.argv[1],int(sys.argv[2]))

        
        
