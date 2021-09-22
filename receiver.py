import io
from socket import *
import pickle
import sys 

class Packet: 
    def __init__(self, ptype, seqnum,length,data) : 
        self.ptype = ptype 
        self.seqnum=seqnum
        self.length = length
        self.data = data
        
    def get_ptype(self): 
        return self.ptype 
    
    def get_seqnum(self): 
        return self.seqnum
    
    def get_length(self): 
        return self.length
    
    def get_data(self):
        return self.data 

def main(send_addr,send_port,recv_port,fname): 
    ##receiving port of the receiver 
    serverPort = recv_port 
    serverSocket =socket(AF_INET,SOCK_STREAM)
    serverSocket.bind (('',serverPort))
    serverSocket.listen(1) 
    print ('Receiver ready to receive from nMulator')     
    

    ##sending port of the sender 
    clientSocket=socket(AF_INET,SOCK_STREAM) 
    clientSocket.connect((send_addr,send_port))    
    print('Receiver ready to send to nMulator')    
    clientSocket.send("receiver connected".encode())
    
    conn,addr = serverSocket.accept()
    serverSocket.settimeout(1000)
    
    ack_received = [0] *30
    finished = [1] *30
    list_of_packets = [0] * 30
    
    arrival_log = open("arrival.log",'w')
    
    while (True): 
        ##receiving from nmulator
        data= conn.recv(4096)
    
        ##unpack the data 
        data_variable = pickle.loads(data)
        
        ##if its  packet 
        if (data_variable.get_ptype() == 1) : 
            received = data_variable.get_seqnum()
            

            ##if its not received yet 
            if ack_received[received] == 0:
                ack_received[received] = 1
                
                arrival_log.write("{0}\n".format(received))
            
                ##send back the ack package 
                temp_packet=Packet(0,received,0,'')
                data_string = pickle.dumps(temp_packet)
                clientSocket.send(data_string)
                list_of_packets[received] = data_variable
                
            ##if we already received     
            elif ack_received[received] == 1: 
                temp_packet=Packet(0,received,0,'')
                data_string = pickle.dumps(temp_packet)
                clientSocket.send(data_string)
                
            else:
                continue 
        ##receiving EOT packet
        elif data_variable.get_ptype() == 2:
            print("EOT received")
            if ack_received == finished:
                print("loop broken, no longer receiving ")
                break
             
            else:
                continue 
        else: 
            continue 
    
    ##writing to file 
    saved_file = open(fname,'w')
    for i in list_of_packets: 
        temp_string = i.get_data()
        saved_file.write(temp_string)
        
    saved_file.close() 
    clientSocket.close()
    serverSocket.close() 
        
    
main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])        
    
    
