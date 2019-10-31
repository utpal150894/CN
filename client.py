import socket
import os
import subprocess
import pickle


def menu1(s):
    print("1.list all groups")
    print("2.list my groups")
    print("3.leave group")
    print("4.join group")
    print("5.upload")
    print("6.download")
    print("7.list files")
    print("8.show all logs")
    print("9.show all messages")
    print("10.write a message")
    print("11.Go back")
    ch=int(input())
    if ch==11:
        login(s)
    elif ch==1:
        s.send(str.encode("list all groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in groups:
            print(i)
        menu1(s)
    elif ch==2:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(100000))
        for i in groups:
            print(i)
        menu1(s)
    elif ch==3:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            s.send(str.encode("leave "+groups[ch1-1],"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==4:
        s.send(str.encode("list except mine"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            s.send(str.encode("join "+groups[ch1-1],"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==7:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            s.send(str.encode("list files "+groups[ch1-1],"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==8:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            s.send(str.encode("show log "+groups[ch1-1],"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==9:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups






def join(s,groups):
    for i in range(len(groups)):
        print(i+1,".",groups[i])
    print(len(groups)+1,".logout")
    print("choose a group to join")
    ch=[int(i)-1 for i in input().split(' ')]
    #print(ch)
    for i in ch:
        if i<=0 or i>len(groups):
            ch.remove(i)
    print(ch)
    sel_grs=pickle.dumps(ch)
    s.send(sel_grs)
    print(s.recv(1024).decode("utf-8"))
def login(s):
    print("Enter \n 1. login \n 2. Signup \n")
    ch=int(input())
    if ch==1:
        print("Enter username and password \n")
        username=input("username:")
        password=input("password:")
        s.send(str.encode("Login: "+username+"=="+password))
        res=s.recv(1000000).decode("utf-8")
        print(res)
        if res=="login successful":
            menu1(s) 
    else:
        print("Enter username and password \n")
        username=input()
        password=input()
        s.send(str.encode("Signup:"+username+"=="+password))
        res=s.recv(1000000).decode("utf-8")[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            print("Enter a message")
            msg=input()
            s.send(str.encode("show messages "+groups[ch1-1],"utf-8"))
            s.send(str.encode(msg,"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==10:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            print("Enter a message")
            s.send(str.encode("write "+groups[ch1-1],"utf-8"))
            s.send(str.encode(input(),"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==5:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            print(os.listdir())
            print("Enter a file path")
            path=input().split('/')
            fname=path[len(path)-1]
            s.send(str.encode("upload "+groups[ch1-1],"utf-8"))
            s.send(pickle.dumps(fname))
            file=open(path,'r')
            s.send(pickle.dumps(file.read()))
            file.close()
            print(s.recv(1000000).decode("utf-8"))
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)
    elif ch==6:
        s.send(str.encode("list my groups","utf-8"))
        groups=pickle.loads(s.recv(1000000))
        for i in range(len(groups)):
            print(i+1," ",groups[i])
        print("choose a group")
        ch1=int(input())
        if ch1>0 and ch1<=len(groups):
            s.send(str.encode("list files "+groups[ch1],"utf-8"))
            print(s.recv(1000000).decode("utf-8"))
            print("Enter a file name")
            fname=input()
            s.send(str.encode("download "+groups[ch1-1],"utf-8"))
            s.send(str.encode(fname,"utf-8"))
            data=s.recv(1000000).decode("utf-8")
            file=open('./downloads/'+fname,'w')
            file.write(data)
            file.close()
            menu1(s)
        else:
            print("invalid choice")
            menu1(s)






def join(s,groups):
    for i in range(len(groups)):
        print(i+1,".",groups[i])
    print(len(groups)+1,".logout")
    print("choose a group to join")
    ch=[int(i)-1 for i in input().split(' ')]
    #print(ch)
    for i in ch:
        if i<=0 or i>len(groups):
            ch.remove(i)
    print(ch)
    sel_grs=pickle.dumps(ch)
    s.send(sel_grs)
    print(s.recv(1024).decode("utf-8"))
def login(s):
    print("Enter \n 1. login \n 2. Signup \n")
    ch=int(input())
    if ch==1:
        print("Enter username and password \n")
        username=input("username:")
        password=input("password:")
        s.send(str.encode("Login: "+username+"=="+password))
        res=s.recv(1000000).decode("utf-8")
        print(res)
        if res=="login successful":
            menu1(s) 
    else:
        print("Enter username and password \n")
        username=input()
        password=input()
        s.send(str.encode("Signup:"+username+"=="+password))
        res=s.recv(1000000).decode("utf-8")
        print(res)
        if res=="signup succcessful":
            menu1(s)









s = socket.socket()
host = '10.1.135.14'
port = 9999

s.connect((host, port))

while True:
    login(s)
    