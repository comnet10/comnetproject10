# Tcp Chat server
 
import socket, select, sys, string
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2 4096
    PORT = 14376 
    accounts=[] 
    User_ID=open("User_ID.txt","r")
    User_PW=open("User_PW.txt","r")
    User_ID_list=[]
    User_PW_list=[]
    for line in User_ID.readlines():
	User_ID_list.append(line.strip())
    for line in User_PW.readlines():
	User_PW_list.append(line.strip())
    User_ID.close()
    User_PW.close()
    user_id=[]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))	#open port
    server_socket.listen(10)	#How many people connect
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
		### #compare with ID# ###
		log = sockfd		

                if log in CONNECTION_LIST:
			while 1:
				sys.stdout.flush()
				sockfd.send('Write your ID')
 		      		ID = sockfd.recv(RECV_BUFFER)
				sys.stdout.flush()
				sockfd.send('Write your PW')
				PW = sockfd.recv(RECV_BUFFER)
				sys.stdout.flush()
				if ID.strip() in User_ID_list and PW.strip() in User_PW_list: 		
 		    		   	print ID.strip() + ' is in Log-in'
					sockfd.send('1')
					accounts.append(ID.strip())					
					print "Client " + ID.strip() + '@' + "(%s, %s) connected" % addr
				       	break
				else:
					print ID
					sockfd.send('0')
		
			
		broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                 	#
	        	data = sock.recv(RECV_BUFFER)			
			if data:
				i=0
				while 1:
					if CONNECTION_LIST[i] == sockfd:
						break
					i=i+1
 	                        	
				broadcast_data(sock, "\r" + '<' + account[i] + '@' + str(sock.getpeername()) + '> ' + data)
				print '<' + account[i] + '@' + str(sock.getpeername()) + '>' + data.strip()               
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
