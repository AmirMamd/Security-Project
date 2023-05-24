import socket, threading,pickle,re
from EmailsWithMasterKeys import Emails
import os
from Enc_Dec import encrypt_file
import binascii, secrets
class ClientThread(threading.Thread):
    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for ",ip,":",str(port))

    def get_session_key(self):

        key= secrets.token_bytes(16)
        key1=binascii.hexlify(key).decode()
        return key1
    def run(self):
        print ("Connection from : ",ip,":",str(port))
        clientsock.send(pickle.dumps("Welcome to the multi-thraeded server"))
        data = "dummydata"
        while len(data):
            try:
                print("da5al fel try")
                data = pickle.loads(self.csocket.recv(2048))
                print("Client(%s:%s) sent : %s"%(self.ip, str(self.port),data))
                # self.csocket.send(str.encode("You sent me : "+data))
                s = re.split(r'[(]', str(data))
                print("s=",s,s[1],s[2])
                if s[1] in Emails and s[2] in Emails:
                    print("da5al fel if")
                    SK = open("SessionKey.txt", "wb")
                    SK.write(self.get_session_key().encode())
                    SK.close()
                    #session key is taken randomly from the function and used to encrypt
                    # the master key of A and B (Sender and receiver) and put the encryption in SKA and SKB respectively
                    print("line 33")
                    encrypt_file(Emails[s[1]]['masterKey'], 'SessionKey.txt', 'SKA.txt')
                    print("line 34")
                    encrypt_file(Emails[s[2]]['masterKey'], 'SessionKey.txt', 'SKB.txt')
                    print("line 35")
                    with open('SKA.txt', 'rb') as infile:
                        SKA= infile.read()
                        print("line41")
                    with open('SKB.txt', 'rb') as infile:
                        SKB = infile.read()
                        print("line42")
                    combined_data = (SKB, SKA)
                    clientsock.send(pickle.dumps(combined_data))
                    print("line43")
                    # SKA=encrypt_file()
                if data=="quit":
                    self.csocket.send(pickle.dumps("Ok By By"))
                    self.csocket.close()
                    data=''
            except:
                print ("Client at ",self.ip," disconnected...")
                break
host = "127.0.0.1"
port = 4000
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host,port))
while True:
    tcpsock.listen(4)
    print ("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()