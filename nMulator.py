import io
from socket import *
import pickle 
import sys
import random 
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
    
def main(recv_from_sender , recv_addr,send_to_recv,recv_from_recv,sender_addr,send_to_sender,prob,verbose):
    
    ##receiving port for the receiver
    discard_prob = prob * 10 
    serverPort1 = recv_from_recv 
    recv_recv_socket =socket(AF_INET,SOCK_STREAM)
    recv_recv_socket.bind (('',serverPort1))
    recv_recv_socket.listen(1) 
    print ('nMulator ready to receive from recv') 
    
    
    ##receiving port for the sender 
    serverPort2 = recv_from_sender 
    send_recv_socket =socket(AF_INET,SOCK_STREAM)
    send_recv_socket.bind (('',serverPort2))
    send_recv_socket.listen(1) 
    print ('nMulator ready to receive from sender')  
    
    
    recv_conn,recv_addr=recv_recv_socket.accept() 
    recv_signal = recv_conn.recv(1024).decode()
    print(recv_signal)
    
    ##connect send port to recv 
    recv_send_socket=socket(AF_INET,SOCK_STREAM) 
    print(recv_addr)
    print(send_to_recv)
    recv_send_socket.connect((recv_addr[0],send_to_recv))
    print('nMulator ready to send to recv')     
    
    
    send_conn,sender_addr=send_recv_socket.accept() 
    sender_signal = send_conn.recv(1024).decode()
    print(sender_signal)
    
    ##connect send port to sender
    send_send_socket=socket(AF_INET,SOCK_STREAM) 
    send_send_socket.connect((sender_addr[0],send_to_sender))    
    print('nMulator ready to send to sender')        
    
    send_recv_socket.settimeout(1)
    recv_recv_socket.settimeout(1)
    """
    send_recv_socket.setblocking(0)
    recv_recv_socket.setblocking(0)
    """

    ##recv_conn.settimeout(0.5)
    ##send_conn.settimeout(0.5)
    recv_conn.setblocking(0)
    send_conn.setblocking(0)
    
 

    while(True): 
        try:
            
            packet1= send_conn.recv(4096)
            
            data_variable = pickle.loads(packet1)
            if verbose == 1: 
                print("receiving Packet {0}".format(data_variable.get_seqnum()))
            roll = random.randint(0,10)

            ##not discaring eot packet
            if (roll < discard_prob) and (data_variable.get_ptype() != 2):
                if verbose == 1: 
                    print("discarding Packet {0}".format(data_variable.get_seqnum()))
                pass 
            else:
                if verbose == 1: 
                    print("forwarding Packet {0}".format (data_variable.get_seqnum()))
                recv_send_socket.send(packet1)
            
                
                if data_variable.get_ptype() == 2: 
                    break 
                
        except error:

            pass 
        try:
        
            packet2=recv_conn.recv(4096)
        
            
            roll = random.randint(0,10) 
            data_variable = pickle.loads(packet2)
            if verbose == 1: 
                print("receiving ack {0}".format(data_variable.get_seqnum()))

            ##not discarding eot packet 
            if roll < discard_prob and (data_variable.get_ptype() != 2):
                if verbose == 1: 
                    print ("discarding ack {0}".format(data_variable.get_seqnum()))
                pass 
            else: 
                send_send_socket.send(packet2)
                if verbose == 1: 
                    print("forwarding ack {0}".format(data_variable.get_seqnum()))
                data_variable = pickle.loads(packet2)
                
                if data_variable.get_ptype() == 2: 
                    break
                
            
        except error: 
        
            pass 
    return 
            
main(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],int(sys.argv[6]),float(sys.argv[7]),int(sys.argv[8]))    
    
