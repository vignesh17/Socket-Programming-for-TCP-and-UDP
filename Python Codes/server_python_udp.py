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


def sent1(aray, socket_cuttently_under_use, destination_address): # Function is used to keep track of the ACK for the MSG sent and keeps track of number of times MSG is sent
    try:
        socket_cuttently_under_use.sendto(aray, destination_address) # Array is sent to the Specified Destination Address
    except Exception as e1:
        message("Result transmission failed.", socket_cuttently_under_use) # Failure MSG is displayed if the sendto function does not work
    ack = False # Initializing variable ack to false
    count = 0 # Initializing variable count to 0
    socket_cuttently_under_use.settimeout(1) # Setting timeout to 1 second 
    while not ack:
        try:
            if (not ack) & (count == 4): # Checks if there is no ACK and whether client sent it 3 times
                message("Failed to send expression.", socket_cuttently_under_use) # Error MSG is sent
            possible_ACK, the_address = socket_cuttently_under_use.recvfrom(4096) # Recieves ACK from the user
            if possible_ACK == b'ACK': # Checks if the ACK is for the MSG sent
                ack = True
                socket_cuttently_under_use.settimeout(None) # Timeout funcution is executed
                break
        except socket.timeout:
            count += 1 # Counts the number of times the MSG is sent
            if count < 4: # Checks for 3 times MSG sent
                socket_cuttently_under_use.sendto(aray, destination_address) # Length is sent to the Specified Destination Address
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


def exit():  # Function to exit the program
    try:
        sys.exit() # Exits from the user
    except SystemExit:
        os._exit(1) # Exits from the system on the whole


BUFFER_SIZE = 4096
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Connection
if len(sys.argv) != 2: # Checks for the Port Number
    print("Invalid port number. Terminating") # Prints Error MSG if port number is not specified
    exit() # Exits from the user
addr_source = ('itsunix.albany.edu', int(sys.argv[1])) # Connection is established to that Port Number and the socket
socket.bind(addr_source) # Binds the connection
while True: # infinite loop
    try:
        array1, address = socket.recvfrom(BUFFER_SIZE)
        exp = b''
        if array1:
            exp = wait(int(array1), socket, "Did not receive valid expression from client. " "Terminating.") # Gets the expression from the client
            result = b''
            try:
                result = res(exp)
            except Exception as e3: 
                print("Did not receive valid expression from client. Terminating.") # Prints an Error MSG
                exit()
            result_length = len(result) # stores the length of the result
            if result_length > BUFFER_SIZE: # Compares result length with buffer size
                socket.sendto(str(result_length), address) # Length of the result is sent to the Specified Address
                sb = 0  # Initialize the value of sb to 0
                lts = result_length # Initialize the value of lts to result_length
                while lts > BUFFER_SIZE: # Loops until lts becomes greater than buffer_size
                    to_sent = result[sb:BUFFER_SIZE+sb]
                    lts -= BUFFER_SIZE
                    sb += BUFFER_SIZE
                    sent1(to_sent, socket, address) # Send1 function is called
                if lts > 0:
                    sent1(result[sb:], socket, address) # Send1 function is called
            else:
                send(result, socket, address) # Send function is called
    except (ConnectionResetError, socket.timeout) as e:
        continue