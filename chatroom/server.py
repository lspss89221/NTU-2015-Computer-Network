# chat_server.py
 
import sys, socket, select

HOST = '' 
SOCKET_LIST = []
ID_Dict = {}
RECV_BUFFER = 4096 
PORT = 9022

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                print "Client (%s, %s) connected" % addr
                while(not login(sockfd)):
                    continue
                broadcast(server_socket, sockfd, "\r[%s] entered our chatting room\n" % ID_Dict[sockfd])
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + ID_Dict[sock] + '] ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client [%s] is offline\n" % ID_Dict[sock]) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client [%s] is offline\n" % ID_Dict[sock])
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                if ID_Dict.has_key(socket):
                    del ID_Dict[socket]

def login (sock):
    accounts = open('account','r+')
    ID = sock.recv(RECV_BUFFER)
    if (ID == 'NEW'):
        ID = sock.recv(RECV_BUFFER)
        accounts.seek(0, 2)
        accounts.write(ID+'\n')
    else:
        for line in accounts:
            #login success
            if line.find(ID)>=0:
                ID_Dict[sock] = ID[0:ID.find(':')]
                SOCKET_LIST.append(sock)
                sock.send("success")
                return 1
        sock.send("fail")
        return 0
    accounts.close()


if __name__ == "__main__":

    sys.exit(chat_server())