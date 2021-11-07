import socket
import struct

def client(dateTime, hostName, port):
    if (dateTime != 'time' and dateTime != 'date') or hostName != socket.gethostname() or port < 1024 or port > 64000:
        return print("invalid entries, restart client and make sure to enter right values. :)")

    host = socket.gethostbyname(hostName)

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, int(port)))  # connect to the server
    magicNo = 0x497E
    packetType = 0x0001
    if dateTime == 'date':
        requestType = 0x0001
    else:
        requestType = 0x0002
    DT_Request = (magicNo, packetType, requestType)
    packer = struct.Struct('I I I')
    data = packer.pack(*DT_Request)
    DTUnpacker = struct.Struct('I I I I I I I I I')
    while True:
        client_socket.sendall(data)
        client_socket.settimeout(1.0)
        try:

            data1 = client_socket.recv(DTUnpacker.size)
        except client_socket.settimeout():
            return print("data didnt arrive quick enough! :(")
        finally:

            DT_Response = DTUnpacker.unpack(data1)
            data2 = client_socket.recv(2048).decode()
            array = bytearray()
            array += (int(DT_Response[0]).to_bytes(2, byteorder="big"))
            array += (int(DT_Response[1]).to_bytes(2, byteorder="big"))
            array += (int(DT_Response[2]).to_bytes(2, byteorder="big"))
            array += (int(DT_Response[3]).to_bytes(2, byteorder="big"))
            array += (int(DT_Response[4]).to_bytes(1, byteorder="big"))
            array += (int(DT_Response[5]).to_bytes(1, byteorder="big"))
            array += (int(DT_Response[6]).to_bytes(1, byteorder="big"))
            array += (int(DT_Response[7]).to_bytes(1, byteorder="big"))
            array += (int(DT_Response[8]).to_bytes(1, byteorder="big"))
            totalBytes = len(array)
            final_packet = str(DT_Response) + " " +  data2
            if totalBytes >= 13 and DT_Response[0] == 0x497E and DT_Response[1] == 0x0002 and (DT_Response[2] == 0x0001 or DT_Response[2] == 0x0002 or
                                                                                                    DT_Response[2] == 0x0003) and DT_Response[3] < 2100 and 1 <= DT_Response[4] <= 12 and 1 <= DT_Response[5] <= 31 and 0 <= DT_Response[6] <= 23 and 0 <= DT_Response[7] <= 59:
                print("received a valid DT-Response packet")
                print('Received from server: ' + str(final_packet))
                break
            else:
                print("invalid DT-Response packet received")


        client_socket.close()  # close the connection

client(str(input("enter 'date' or 'time': ")), input("enter the name of your computer(eg. 'LAPTOP-EPVUG575'): "),  int(input("choose a port number(any of the three you enetred for the server): ")))  # socket server port number
