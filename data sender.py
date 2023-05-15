import socket
import MetaTrader5 as mt5
import time
import json
import time


minute_dict = {}
hour_dict = {}


#Login to account
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# display data on MetaTrader 5 version
print(mt5.version())

    
# now connect to another trading account specifying the password
account=50913987
authorized=mt5.login(account, password="QAGWUaXv", server="ICMarketsSC-Demo")
if authorized:
    print("Account authorized")

# get the hostname
host = ""
port = 5000  # initiate port no above 1024

server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)
while 1 ==1:
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if data == "data":
            account_info_dict = mt5.account_info()._asdict()
            balance = account_info_dict.get('balance')
            equity = account_info_dict.get('equity')
            data = str(balance)+" , "+str(equity)
            conn.send(data.encode())  # send data to the client
        else:
            break
    conn.close()  # close the connection


