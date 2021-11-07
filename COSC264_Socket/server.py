import socket
import select
import struct
import datetime
def server(english_port, maori_port, german_port):
    for i in [english_port, maori_port, german_port]:
        if i < 1024 or i > 64000:
            return print("invalid port numbers, restart server and make sure all ports are in between 1024 and 64000")
    magicNo = 0x497E
    pakcetTypeResp= 0x0002
    pakcetTypeReq = 0x0001
    languageCodeEnglish = 0x0001
    languageCodeMaori = 0x0002
    languageCodeGerman = 0x0003
    englishMonths = ["January", "February", "March", "April", "May", "June", "July",
                     "August", "September", "October", "November", "December"]
    germanMonths = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                    "August", "September", "Oktober", "November", "Dezember"]
    maoriMonths = ["Kohitātea", "Hui-tanguru", "Poutū-te-rangi", "Paenga-whāwhā", "Haratua", "Pipiri", "Hōngongoi",
                   "Here-turi-kōkā", "Mahuru", "Whiringa-ā-nuku", "Whiringa-ā-rangi", "Hakihea"]
    host = socket.gethostname()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, english_port))  # bind host address and port together
    server_socket2.bind((host, maori_port))  # bind host address and port together
    server_socket3.bind((host, german_port))  # bind host address and port together
    server_socket3.listen(5)
    server_socket2.listen(5)
    server_socket.listen(5)
    # configure how many client the server can listen simultaneously
    inputs = [server_socket3, server_socket2, server_socket]
    outputs = []

    print('waiting for the next event')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    while True:
        for s in readable:
            unpacker = struct.Struct('I I I')
            if s is server_socket:
                connection, client_address = s.accept()
                print('new connection from' + str(client_address))
                while True:
                    # A "readable" server socket is ready to accept a connection
                    inputs.append(connection)
                    data = connection.recv(unpacker.size)
                    DT_request = unpacker.unpack(data)
                    array = bytearray()
                    array += (int(DT_request[0]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[1]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[2]).to_bytes(2, byteorder="big"))
                    totalBytes = len(array)
                    if DT_request[0] == magicNo and DT_request[1] == pakcetTypeReq and (
                            DT_request[2] == 0x0001 or DT_request[2] == 0x0002) and totalBytes == 6:
                        print("server received valid DT-Request packet!")
                        if DT_request[2] == 0x0001:
                            print("client wants current date in English")
                            currentTime = datetime.datetime.now()
                            message = "Today's date is {} {}, {}".format(englishMonths[currentTime.month-1], currentTime.day, currentTime.year)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeEnglish, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                        else:
                            print("client wants time of day in English")
                            currentTime = datetime.datetime.now()
                            if currentTime.minute > 9:
                                message = "The current time is {}:{}".format(currentTime.hour, currentTime.minute)
                            else:
                                message = "The current time is {}:0{}".format(currentTime.hour, currentTime.minute)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeEnglish, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                    else:
                        print("server received invalid DT-Request packet")

                    server_socket.close()


            if s is server_socket2:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                print('new connection from' + str(client_address))
                while True:
                    inputs.append(connection)
                    data = connection.recv(unpacker.size)
                    DT_request = unpacker.unpack(data)
                    array = bytearray()
                    array += (int(DT_request[0]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[1]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[2]).to_bytes(2, byteorder="big"))
                    totalBytes = len(array)
                    if DT_request[0] == magicNo and DT_request[1] == pakcetTypeReq and (
                            DT_request[2] == 0x0001 or DT_request[2] == 0x0002) and totalBytes == 6:
                        print("server received valid DT-Request packet!")
                        if DT_request[2] == 0x0001:
                            print("client wants current date in Maori")
                            currentTime = datetime.datetime.now()
                            message = "Ko te ra o tenei ra ko {} {}, {}".format(maoriMonths[currentTime.month - 1],
                                                                                currentTime.day, currentTime.year)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeMaori, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                        else:
                            print("client wants time of day in Maori")
                            currentTime = datetime.datetime.now()
                            if currentTime.minute > 9:
                                message = "Ko te wa o tenei wa {}:{}".format(currentTime.hour, currentTime.minute)
                            else:
                                message = "Ko te wa o tenei wa {}:0{}".format(currentTime.hour, currentTime.minute)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeMaori, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                    else:
                        print("server received invalid DT-Request packet")
                    server_socket2.close()


            if s is server_socket3:
                connection, client_address = s.accept()
                print('new connection from' + str(client_address))
                while True:
                    inputs.append(connection)
                    data = connection.recv(unpacker.size)
                    DT_request = unpacker.unpack(data)
                    array = bytearray()
                    array += (int(DT_request[0]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[1]).to_bytes(2, byteorder="big"))
                    array += (int(DT_request[2]).to_bytes(2, byteorder="big"))
                    totalBytes = len(array)
                    if DT_request[0] == magicNo and DT_request[1] == pakcetTypeReq and (
                            DT_request[2] == 0x0001 or DT_request[2] == 0x0002) and totalBytes == 6:
                        print("server received valid DT-Request packet!")
                        if DT_request[2] == 0x0001:
                            print("client wants current date in German")
                            currentTime = datetime.datetime.now()
                            message = "Heute ist der {}. {} {}".format(currentTime.day,
                                                                       germanMonths[currentTime.month-1], currentTime.year)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeGerman, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                        else:
                            print("client wants time of day in German")
                            currentTime = datetime.datetime.now()
                            if currentTime.minute > 9:
                                message = "Die Uhrziet ist {}:{}".format(currentTime.hour, currentTime.minute)
                            else:
                                message = "Die Uhrziet ist {}:0{}".format(currentTime.hour, currentTime.minute)
                            if len(message) > 255:
                                print("message too long")
                                continue
                            array = bytearray()
                            mybytes = message.encode('utf-8')
                            array += mybytes
                            DT_response = (magicNo, pakcetTypeResp, languageCodeGerman, currentTime.year, currentTime.month, currentTime.day,
                                           currentTime.hour, currentTime.minute, len(message))
                            packer = struct.Struct('I I I I I I I I I')
                            data = packer.pack(*DT_response)
                            connection.send(data)
                            connection.send(mybytes)
                            connection.close()
                            break
                    else:
                        print("server received invalid DT-Request packet")
                    server_socket3.close()
        server_socket2.close()
        server_socket.close()
        server_socket3.close()
        break


server(int(input("enter english port: ")), int(input("enter moari port: ")), int(input("enter german port: ")))
