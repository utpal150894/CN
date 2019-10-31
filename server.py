import socket
import sys
import threading
import time
from queue import Queue
import os
import pickle
import subprocess

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

def run_command(cmd):
    process = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')

def append(path,line):
    f=open(path,'a')
    f.write(line+'\n')
    f.close()

def get_group(l,ind):
    return " ".join(l[ind:])


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        
        s.listen(50)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            all_connections.append(conn)
            all_address.append(address)
            x=threading.Thread(target=thread_function,args=(s,conn,address,))
            print("Connection has been established :" + address[0])
            x.start()
        except:
            print("Error accepting connections")



def thread_function(s,conn,address):
    username=""
    while True:
        client_response=conn.recv(20480).decode("utf-8")
        #print(client_response)
        if client_response.startswith("Signup:"):
            #print("utpal podder poddr\n")
            atpos=client_response.find(':')
            sppos=client_response.find('==',atpos)
            userId=client_response[atpos+1:sppos]
            putUserLogDetail=client_response[atpos+1:]
            putUserLogDetail=putUserLogDetail+"\n"
            try:
                fhand=open("login.text")
            except:
                print("File cannot be opened:",fhand)
                exit()
            l=[]
            for line in fhand:
                spposFileRow=line.find('==')
                userIdFileRow=line[:spposFileRow]
                l.append(userIdFileRow)
            fhand.close()
            if userId in l:
                conn.send(str.encode("The user_name already exists"))
            else:
                fhand=open("login.text","a")
                fhand.write(putUserLogDetail)
                fhand.close()
                conn.send(str.encode("signup succcessful"))
                username=userId
                groups=os.listdir("./groups")
                dirs=pickle.dumps(os.listdir("./groups"))
                conn.send(dirs)
                sel_grs=pickle.loads(conn.recv(1024))
                for i in sel_grs:
                    fhand=open("./groups/"+groups[i-1]+"/members.txt","a")
                    fhand.write(username)
                    fhand.close()
                conn.send("success:joining successful")
        elif client_response.startswith("Login: "):
            atpos=client_response.find(':')
            sppos=client_response.find("==",atpos)
            userId=client_response[atpos+2:sppos]
            userPass=client_response[sppos+2:len(client_response)]
            #print(userId)
            #print(userPass)
            userPass=int(userPass)
            #print(type(userPass))
            try:
                fhand=open("login.text")
            except:
                print("File cannot be opened:",fhand)
                exit()
            l=[]
            for line in fhand:
                spposFileRow=line.find("==")
                userIdFileRow=line[:spposFileRow]
                l.append(userIdFileRow)
            fhand.close()
            #print(l)
            #l.pop()
            print(l)
            if userId in l:
                #print("userId is present:\n")
                count1=1
                for Id in l:
                    if Id!=userId:
                        count1=count1+1
                    else:
                        break
                #print(count1)
                try:
                    fhand=open("login.text")
                except:
                    print("File cannot be opened:",fhand)
                    exit()
                count2=1
                for line in fhand:
                    #print(count2)
                    if count2!=count1:
                        count2=count2+1
                    else:
                        #print(count2)
                        #print("utpal")
                        atposFileRow=line.find("=")
                        passFileRow=line[atposFileRow+2:]
                        passFileRow=int(passFileRow)
                        print(passFileRow)
                        if passFileRow!=userPass:
                            conn.send(str.encode("password is wrong"))
                            #print("password is wrong")
                            break
                        else:
                            username=userId
                            conn.send(str.encode("login successful"))
                            break
                fhand.close()
            else:
                conn.send(str.encode("wrong user Id"))
                #print("wrong user Id")
        elif client_response.startswith("list all "):
            groups=run_command(["ls","./groups"])
            l=[]
            print("groups ",groups)
            for i in groups.split(' '):
                l.append(i)
            l1=pickle.dumps(l)
            conn.send(l1)
        elif client_response.startswith("list my "):
            groups=run_command(["ls","./groups"])
            l=[]
            for i in groups.split('\n'):
                mems=run_command(["cat","./groups/"+i+"/members.txt"])
                if username in mems:
                    l.append(i)
            l1=pickle.dumps(l)
            conn.send(l1)
        elif client_response.startswith("list except "):
            groups=run_command(["ls","./groups"])
            l=[]
            for i in groups.split('\n'):
                mems=run_command(["cat","./groups/"+i+"/members.txt"])
                for j in mems.split('\n'):
                    if j==username:
                        print(j+" "+username)
                        break
                else:
                    print("appended")
                    l.append(i)
            l1=pickle.dumps(l)
            conn.send(l1)
        elif client_response.startswith("show log "):
            group=get_group(client_response.split(' '),2)
            conn.send(str.encode(run_command(["cat" ,"./groups/"+group+"/log.txt"]),"utf-8"))
        elif client_response.startswith("show messages "):
            group=get_group(client_response.split(' '),2)
            conn.send(str.encode(run_command(["cat", "./groups/"+group+"/log.txt"]),"utf-8"))
        elif client_response.startswith("write "):
            group=get_group(client_response.split(' '),1)
            msg=conn.recv(1000000).decode("utf-8")
            append('./groups/'+group+'/messages.txt',username+" : "+msg)
        elif client_response.startswith("list files"):
            group=get_group(client_response.split(' '),1)
            files=run_command(["ls","./groups/"+group+"/files"])
            conn.send(str.encode(files,"utf-8"))
        elif client_response.startswith("join"):
            group=get_group(client_response.split(' '),1)
            append('./groups/'+group+'/members.txt',username)
            conn.send(str.encode("joining successful","utf-8"))
        elif client_response.startswith("leave"):
            group=get_group(client_response.split(' '),1)
            data=''
            with open("./groups/"+group+"/members.txt","r") as f:
                for line in f:
                    if username not in line:
                        data+=line+'\n'
            
            with open("./groups/"+group+"/members.txt","w") as f:
                f.write(data)
            conn.send(str.encode("leaving successful","utf-8"))
        elif client_response.startswith("upload "):
            group=get_group(client_response.split(' '),1)
            filename=pickle.loads(conn.recv(1000000))
            print('./groups/'+group+'/files/'+filename)
            data=pickle.loads(conn.recv(1000000))
            print(data +" received")
            file=open('./groups/'+group+'/files/'+filename,'w+')
            file.write(data)
            file.close()
        elif client_response.startswith("download "):
            group=get_group(client_response.split(' '),1)
            filename=conn.recv(1000000).decode("utf-8")
            file=open('./groups/'+group+'/files/'+filename,'r')
            conn.send(str.encode(file.read(),"utf-8"))
            file.close()



                

create_socket()
bind_socket()
accepting_connections()
