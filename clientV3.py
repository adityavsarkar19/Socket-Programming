# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 03:36:42 2021

@author: Aditya Sarkar
"""
import socket 


PORT = 5545
SERVER = socket.gethostbyname(socket.gethostname())
#FORMAT = 'utf-8'

#print (SERVER)
#Server in my pc is 192.168.137.1


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP of Local host
client_socket.connect((SERVER, PORT))

server_reply = client_socket.recv(1024).decode()
print(server_reply)

while True:

    Choice = input("Enter your choice (1/2/3): ")
    client_socket.send(Choice.encode())

    if Choice == '3':
        
        print("Disconnected from server........")
        break

    elif Choice == '1':
        UserID = input("Enter your Ashoka Email ID: ")
        while '@ashoka.edu.in' not in UserID:
            UserID = input("Not a valid Ashoka Email ID, REenter your Ashoka Email ID: ")
            
        client_socket.send(UserID.encode())
        status = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        if status == 'NEW':
            print("A New User! Your Password is: ",password)
            break
        else:
            PW=input("Enter your password: ")
            if PW != password:
                print("Wrong Password! Quiting..!")
                break
            
        
        
        
        vote = client_socket.recv(1024).decode()
        vote_ch = client_socket.recv(1024).decode()
        print(vote)
        print(vote_ch)
        if vote_ch == '1':
            vote_for = input("Enter your vote (A/B/C) to vote:")
            while vote_for not in "ABCabc":
                vote_for = input("Invalid Choice! Enter Again: ")
            client_socket.send(vote_for.encode())
                

        # reply from server 
        server_reply = client_socket.recv(1024).decode()
        print(server_reply)
        break
    
    elif Choice == '2':
        UserID = input("Enter your Ashoka Email ID: ")
        while '@ashoka.edu.in' not in UserID:
            UserID = input("Not a valid Ashoka Email ID, REenter your Ashoka Email ID: ")
        client_socket.send(UserID.encode())
        
        status = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        if status == 'OLD':
            PW=input("Enter your password: ")
            if PW != password:
                print("Wrong Password! Quiting..!")
                break
        else:
            print("Not a valid user! Quiting...")
            break
	# reply from server 
        server_reply = client_socket.recv(1024).decode()
        print(server_reply)
        break

    else:
        print("Invalid Choice!")

client_socket.close()
