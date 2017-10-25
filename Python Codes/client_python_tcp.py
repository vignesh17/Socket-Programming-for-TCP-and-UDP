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


def add():  # Function to get the Server Name or IP Address and Port Number and to validate the Port Number
    name = raw_input("Enter server name or IP address: ") # Gets the Server Name or IP Address from the user
    num = int(raw_input("Enter port: ")) # Gets the Port Number from the user
    if (num < 0) | (num > 65535): # Checks for the valid Port Number
        print("Invalid port number. Terminating.") # If the Port Number is invalid
        exit()
    addr = (name, num) # A new Tuple is created with the given Name and Port Number
    return addr # Returns the address


def exit():  # Function to exit the program
    try:
        sys.exit() # Exits the connection
    except SystemExit: # If any error thrown by sys.exit()
        os._exit(1) # Exits from the system on the whole


BUFFER_SIZE = 8192 # Initializes buffer size to 8192
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Connection 
sa = add() # Connects to a particular Port Number
try:
    socket.connect(sa) # Connection is established
except Exception as v: # Connection not Established
    print("Could not connect to server. Terminating.")
    exit()
try:
    exp = raw_input("Enter Expression: ")   # Gets the expression from the user
    l = str(len(exp))  # Stores the length of the expression
    socket.sendall(l)  # Sends the length
    socket.sendall(exp)  # Sends the expression
    response = res(exp) # Expects for the result and stores in response
    expected = len(response)  # Returns the length of the recieved expression
    data = b''   # Stores the value
    while len(data) != expected:
        data += socket.recv(16)
    if data.__eq__(response): # Checks data and response
        print(data)  # Print data
    else:
        print("Could not fetch result. Terminating.") # Prints the statement
        exit() # System Exits
finally:
    socket.close() # Connection is terminated