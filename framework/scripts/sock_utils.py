import socket as s

class buffer:

    def __init__(self,s):
        self.sock = s
        self.buffer = b''

    def get_bytes(self,n):
        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data

        data,self.buffer = self.buffer[:n],self.buffer[n:]
        return data

    def get_utf8(self):
        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data

        data,_,self.buffer = self.buffer.partition(b'\x00')
        # print("data: ", data)
        return data.decode()

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
