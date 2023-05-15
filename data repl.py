import socket
venus_ip = "3.85.50.162"
server_ip = "18.215.177.229"

def client_program():
    x = input("Server or Venus: ").upper 
    if x == "V":
        host = venus_ip
    elif x == "S":
        host = server_ip
    else:
        print("wrong shit")
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
