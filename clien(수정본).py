# telnet program example
import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":

    log='0'
    ID='0'
    PW='0'
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages' 
    if log=='0':
    	while 1:
		sys.stdout.flush()
		data = s.recv(4096)    
		print data
		sys.stdout.flush()
		ID=raw_input("ID : ")
	       	s.send(ID)
	       	sys.stdout.flush()
		data = s.recv(4096)    
		print data		
	       	PW=raw_input("PW : ")	 		
		s.send(PW)
		sys.stdout.flush()
		data = s.recv(4096)
		log = data
		print data
		if log=='1':
			print 'You are in Log-in'
			break
    prompt()

    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096) #4096
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
		msg = sys.stdin.readline()
                s.send(msg)
                prompt()
