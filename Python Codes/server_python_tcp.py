# https://pymotw.com/2/socket/tcp.html
# http://stackoverflow.com/a/13723190
# http://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm


import socket
import sys
import os


def res(expr): # Function that returns the expression
    try:
        result = eval(expr)
        result_int = int(result)
        result_str = str(result)
        result_str += "\n"
        for i in range(0, (result_int-1)): # An iterative loop for i ranging from 0 to (result_int) - 1
            result_str += "Socket Programming\n"
        if result_int != 0:
            result_str += "Socket Programming"
        return result_str # Returns the Expression user sent
    except Exception as v: # For Invalid Expression
         print "Invalid Exeption"  
         exit()


def exit():  # Function to exit the program
    try:
        sys.exit() # Exits the connection
    except SystemExit: # If any error thrown by sys.exit()
        os._exit(1) # Exits from the system on the whole
        

BUFFER_SIZE = 4096
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Connection
if len(sys.argv) != 2: # Checks for the Port Number
    print("Invalid port number. Terminating") # Prints Error MSG if port number is not specified
    exit() # Exits from the user
server_address = ('itsunix.albany.edu', int(sys.argv[1])) # Connection is established to that Port Number and the socket
socket.bind(server_address) # Binds the connection
socket.listen(1) # Waits fr 1 second 
received_string = b'' # Stores the value
while True: # Infinite loop
    connection, client_address = socket.accept() # Waits for the connection between client and server
    try:

        size = connection.recv(sys.getsizeof(int()))
        data = connection.recv(16) # Recieves the datas
        while len(data) != int(size): # A continous loop conparing the size of the data length and size
            if data:
                received_string += data # Collects and Stores the data received
            else:
                break
            data = connection.recv(16)

    finally:
        connection.sendall(res(data)) # Sends the data to the client
        connection.close() # Closes all the conection