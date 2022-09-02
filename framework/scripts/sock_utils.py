import socket as s

def create_tcp_server_socket(address, port, queue_size):
	"""
	Creates a TCP server socket where connection of clients are accepted.

	Args:
		address ([str]): origin address
		port ([int]): port where the server attends all connection requests
		queue_size ([int]): max number of requests in a connection 

	Returns:
		[socket]: TCP server socket 
	"""
	try: 
		sock = s.socket(s.AF_INET, s.SOCK_STREAM)
		sock.bind((address,port))
		sock.listen(queue_size)
		return sock
	except s.error as e:
		print("Error creating socket: ", e)

def create_tcp_client_socket(address, port):
	"""
	Creates a socket where the client communicates with the server.

	Args:
		address ([str]): server's address
		port ([int]): port where server attends all new connection requests

	Returns:
		[socket]: socket where the client communicates with the server
	"""
	try:
		sock = s.socket(s.AF_INET, s.SOCK_STREAM)
		sock.connect((address, port))
		return sock
	except s.error as e:
		print("Error creating socket: ", e)

def receive_all(socket, length):
	"""
	Receives a max number of bytes through the socket

	Args:
		socket ([socket]): connection socket
		length ([int]): number of bytes that should be read

	Returns:
		[str]:  Message received from the connection socket in bytes
	"""
	try: 
		msg = socket.recv(length)
		return msg
	except s.error as e:
		print("Error creating socket: ", e)
