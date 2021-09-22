from socket import *
import io 
import pickle 
import sys 
import time 

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

def main(send_addr,send_port,recv_port,timeout,fname): 
    ##receiving port of the sender 
    serverPort = recv_port 
    serverSocket =socket(AF_INET,SOCK_STREAM)
    serverSocket.bind (('',serverPort))
    serverSocket.listen(1) 
    print ('Sender ready to receive from nMulator')     
    
    ##sending port of the sender 
    clientSocket=socket(AF_INET,SOCK_STREAM) 
    clientSocket.connect((send_addr,send_port))    
    print('Sender ready to send to nMulator')
    clientSocket.send("sender connected".encode())
    
    ##open the file we want to transfer 
    seq_list = open("seqnum.log",'w')
    ack_list = open("ack.log",'w')
    f= open(fname,'r')
    list1= []
    for x in f: 
        list1.append(x) 
    
    flat_list = ''
    for i in list1: 
        flat_list = flat_list + i
    
        
    n=500
    a=[flat_list[i:i+n] for i in range(0, len(flat_list), n)] 
    ##prepare the packets to send 
    list_of_packet = []
    for i in range(30):
        temp_data = flat_list[0:500]
        
        temp_packet = Packet(1,i,500,temp_data)
        flat_list = flat_list[500:]
        list_of_packet.append(temp_packet)
        
    ##send the data 
    list_of_ack =[0]*30
    finished=[1]*30
    conn,addr = serverSocket.accept()
    serverSocket.settimeout(1000)
    conn.settimeout(1)
    for i in list_of_packet:
        data_string = pickle.dumps(i) 
        clientSocket.send(data_string) 
        seq_list.write("{0}\n".format(i.get_seqnum()))
        time.sleep(0.5)
        try:
            data1=conn.recv(4096)
            data_variable1 = pickle.loads(data1)
            if data_variable1.get_ptype() == 0: 
                received1=data_variable1.get_seqnum()
                list_of_ack[received1] = 1
                ack_list.write("{0}\n".format(received1))
    
        except error: 
            pass 
    
    
    
    ##check if we received all the ACK
    ##SET TIME OUT 
    serverSocket.settimeout(timeout)
    
    ##send all the unacknowledged packets 
    if list_of_ack == finished: 
        temp_packet2 = Packet(2,31,0,'')
        data_string2= pickle.dumps(temp_packet2)
        clientSocket.send(data_string2)
        seq_list.close()
        ack_list.close()
        f.close()
        print("EOT packet sent")
        return 
    while True:
        ##check for incoming ACK 
        try:
            data= conn.recv(4096) 
            data_variable = pickle.loads(data) 
            if data_variable.get_ptype() == 0: 
                received = data_variable.get_seqnum()
                list_of_ack[received] = 1
                ack_list.write("{0}\n".format(received))
                if list_of_ack == finished: 
                    temp_packet = Packet(2,31,0,'')
                    data_string1 = pickle.dumps(temp_packet)
                    clientSocket.send(data_string1)
                    ack_list.write("31")
                    print("EOT PACKET SENT")
                    break
                
            elif data_variable.get_ptype() == 2: 
                if list_of_ack == finished:

                    break 
                else:
                    continue 
            else:
                continue 
        ##no incoming ACK 
        except error: 
            ##resend all the packets that dont have ack yet 
            for i in range(30): 
                if list_of_ack[i] == 0: 
                    data_string1 = pickle.dumps(list_of_packet[i])
                    clientSocket.send(data_string1)
                    seq_list.write("{0}\n".format(i))
                    
    seq_list.close()
    ack_list.close()
    f.close() 
    return 
    
                
main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5])        
        
    
    
    
