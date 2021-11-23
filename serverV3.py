# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:36:00 2021

@author: Aditya Sarkar
"""

import socket 
import threading 
import re
import getmac
import datetime
import random

PORT = 5545
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

#print (SERVER)
#Server in my pc 192.168.137.1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER, PORT))

valid_votes = {}
Users={}
# Assume the voting period is from 9:00 AM to 7:00 PM
voting_starts = datetime.time(9, 00)
voting_ends = datetime.time(23, 00)

def voting_time(validity):     
    now = datetime.datetime.now().time()
    current_time = datetime.time(now.hour, now.minute, now.second)

    if validity == "allowed":
        if voting_starts <= current_time <= voting_ends:
            return True
        else:
            return False
   
    if validity == "over":
        if current_time > voting_ends:
            return True
        else:
            return False


def count_votes():
    CountA,CountB,CountC = 0, 0, 0
    for candidate, vote in valid_votes:
        if vote in 'aA':
            CountA += 1
        if vote in 'bB':
            CountB += 1
        if vote in 'cC':
            CountC += 1
    
    Final_Result = "The number of responses/votes each candidates has received as:\nCandidate A: " + str(CountA) + "\nCandidate B: " + str(CountB) + "\nNOTA: " + str(CountC)+"\n" 
    
    if CountA>CountB:
        Final_Result = Final_Result + "\n\nCandidate A has Won!"
    elif CountA<CountB:
        Final_Result = Final_Result + "\n\nCandidate B has Won!"
    else:
        Final_Result = Final_Result + "\n\nUndecided! Both candidates secured the same votes."

    
        
    return Final_Result

def proc(csocket,IP):
     # A Dictionary of AshokaUserID as Keys and Password as Values
    MACID = getmac.get_mac_address(ip=IP)

    welcome_message = "\nWelcome! \nYou can participate in the vote by presenting your password. \nReply with a ”1” if you want to participate now; \nwith a ”2” if you want to see the results; \nand with ”3” other wise."

    csocket.send(welcome_message.encode())

    # receiving client choice
    Choice = csocket.recv(1024).decode()

    if Choice == '1':
        UN = csocket.recv(1024).decode()
        if UN in Users:
            #print(Users)
            csocket.send('OLD'.encode())
            csocket.send(Users[UN].encode())
            
        else:
            #print(Users)
            password=str(random.randint(1000,9999))
            Users[UN]=password
            csocket.send('NEW'.encode())
            csocket.send(password.encode())
            
            
            
        if voting_time("allowed"):
            # to ensure only one vote per user
            if MACID not in valid_votes:
                CANDIDATES = "\n\nEnteer the following keys to votet: \nA to Vote Candidate A \nB to Vote Candidate B\nC for NOTA - None Of The Above\n"                         
                
                csocket.send(CANDIDATES.encode())
                Ch = '1'
                csocket.send(Ch.encode())

                vote = csocket.recv(1024).decode()

                valid_votes.update({MACID: vote})
                Reply = "\n”Thank you for participating. Your response is registered against your IP address - " + str(SERVER)

            else:
                Reply = str(MACID)+" already casted vote. "

        else:
            Reply = "You cannot participate in the vote at the moment."

    if Choice == '2':
        UN = csocket.recv(1024).decode()
        if UN in Users:
            #print(Users)
            csocket.send('OLD'.encode())
            csocket.send(Users[UN].encode())
            
        else:
            #print(Users)
            csocket.send('NEW'.encode())
            csocket.send('invalid'.encode())
        
        
        
        
        if voting_time("over"):
            Reply = count_votes()

        else:
            Reply = "The voting is not over yet. Try after "+str(voting_ends)

    csocket.send(Reply.encode())
    csocket.close()


valid_votes = {}  # a Python dictionary as { MACID: vote}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER,PORT))
server_socket.listen()



def startServer():
    server_socket.listen()
   

while True:
    (csocket, address) = server_socket.accept()
    IP = address[0]
    #Port = address[1]
    #Thread(target=proc, args=(csocket, IP)).start()
    thread = threading.Thread(target = proc, args = (csocket, IP))
    thread.start()


print('Starting server....')
startServer()

