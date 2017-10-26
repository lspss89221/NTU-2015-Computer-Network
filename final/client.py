# chat_client.py

import sys, socket, select
RECV_BUFFER = 4096 

def chat_client():
    #if(len(sys.argv) < 3) :
    #    print 'Usage : python chat_client.py hostname port'
    #    sys.exit()

    host = "localhost"
    port = 9022
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to server.'
    login = False
    while(not login):
        print 'Type your username and password, "NEW" for register!'
        username = raw_input("Username: ")
        if(username=='NEW'):
            s.send('NEW')
            username = raw_input("New Username: ")
            password = raw_input("New Password: ")
        else:
            password = raw_input("Password: ")
        msg = username+':'+password
        s.send(msg)
        log = s.recv(RECV_BUFFER)
        if(log=='success'):
            print 'Login successed, start to chat~~~'
            login = True
        else:
            print 'Login failed!'
    sys.stdout.write('[Me] '); sys.stdout.flush()
    while 1:
        socket_list = [sys.stdin, s]
        #print socket_list
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(RECV_BUFFER)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
