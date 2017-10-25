# https://pymotw.com/2/socket/udp.html
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


def message(msg, socket): # Function used to display various Error MSG
    socket.settimeout(None)
    print(msg + " Terminating.") # Prints the Error MSG
    try:
        socket.close() # Socket Connection is closed
    except Exception as e:
        pass  
    finally:
        exit() # System is Exited


def send(aray, socket, destination_address, failure_error="", time_out_error=""): # Function is used to keep track of the ACK for the MSG sent and keeps track of number of times MSG and Length of the MSG is sent 
    length = str(len(aray)) # Stores the length of the array
    socket.sendto(length, destination_address) # Length is sent to the Specified Destination Address
    try:
        socket.sendto(aray, destination_address) # Array is sent to the Specified Destination Address
    except Exception as e:
        message(failure_error, socket) # Failure MSG is displayed if the sendto function does not work
    ack = False # Initializing variable ack to false
    count = 0 # Initializing variable count to 0
    socket.settimeout(1) # Setting timeout to 1 second 
    while not ack:
        try:
            if (not ack) & (count == 4): # Checks if there is no ACK and whether client sent it 3 times
                message(time_out_error, socket) # Error MSG is sent
            ACK, address = socket.recvfrom(4096) # Recieves ACK from the user
            if ACK == b'ACK': # Checks if the ACK is for the MSG sent
                ack = True
                socket.settimeout(None) # Timeout funcution is executed
                break
        except socket.timeout:
            count += 1 # Counts the number of times the MSG is sent
            if count < 4: # Checks for 3 times MSG sent
                socket.sendto(length, destination_address) # Length is sent to the Specified Destination Address
                socket.sendto(aray, destination_address) # Array is sent to the Specified Destination Address
    return ack # Returns back the ACK


def wait(length, socket, failure_error="", time_out_error=""): # Function is used to check whether the correct array of length is received and sends ACK
    full_expression = b''
    socket.settimeout(0.5) # setting timeout to 0.5 seconds or 500 milliseconds
    while True:
        try:
            data, address = socket.recvfrom(BUFFER_SIZE) # Recieves the array from the sender
            full_expression += data
            if len(full_expression) == length: # Conpares the length of the received array with standard length
                socket.settimeout(None)
                socket.sendto(b'ACK', address) # ACK is sent for the MSG received
                return full_expression
        except socket.timeout:
            message(time_out_error, socket) # Timeout Error MSG is printed
        except Exception:
            message(failure_error, socket) # Failure Error MSG is printed


def receive(length, socket, error_message="", time_out_error=""): # Function is used to get expression that are even longer than buffer size.
    fe = b''
    if length > BUFFER_SIZE: # Compares the length and buffer size
        rb = 0
        btr = length
        while btr > BUFFER_SIZE: # Compares btr and buffer size
            rb1 = BUFFER_SIZE
            fe += wait(rb1, socket, error_message, time_out_error) # wait function is called
            rb += rb1
            btr -= rb1
        if btr > 0:
            rb1 = btr
            fe += wait(rb1, socket, error_message, time_out_error) # wait function is called
        if len(fe) == length: # Checks length with length of fe
            return fe
        else:
            return None
    else:
        return wait(length, socket) # wait function is called


def exit():  # Function to exit the program
    try:
        sys.exit() # Exits the connection
    except SystemExit: # If any error thrown by sys.exit()
        os._exit(1) # Exits from the system on the whole


BUFFER_SIZE = 4096
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP is created
socket.settimeout(1) # Setting timeout to 1 second 
sa = add() # Checks for the valid port number
socket.settimeout(None)
exp = raw_input("Enter expression: ") # Gets the expression from the user
send(exp, socket, sa, "Could not connect to server.", "Failed to send expression.")
data, server = socket.recvfrom(BUFFER_SIZE) # Receives the length of the expression
l = int(data)
if l > BUFFER_SIZE: # Compares l and buffer_size
    rm = receive(l, socket, "Could not fetch result.", "Could not fetch result.") # receive function is called if size is greater
else: 
    rm= wait(l, socket, "Could not fetch result.", "Could not fetch result.") # wait function is called if size is lesser
if len(rm) != l:
    message("Could not fetch result.", socket) # Error MSG is printed
try:
    if rm != res(exp):
        message("Could not fetch result.", socket) # Error MSG is printed
    print(rm)
except Exception as e:
    message("Invalid equation", socket) # Error MSG is printed
socket.close() # Connection is terminated