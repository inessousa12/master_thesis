import datetime, sock_utils, pickle, struct

class Server:
    """
    Class to communicate with a TCP server. It implements methods to establish a connection,
    to send a message and to end the connection.
    """

    def __init__(self, address, port):
        """
        Initializes the class with parameters for future reference.

        Args:
            address ([string]): origin address
            port ([int]): port where server attends all new connection requests
        """
        self._address = address
        self._port = port
        self._conn = None
        self._msg_bytes = 0

    def connect_message(self):
        """
        Establishes a connection with the server specfied in the creation of the object.
        Returns server socket.
        """
        self._conn = sock_utils.create_tcp_client_socket(self._address, self._port)
        now = datetime.datetime.now()
        print(f'[{now:%Y-%m-%d %H:%M:%S}] Client connected (' + self._address + ", " + str(self._port) + ")")
        return self._conn

    def disconnect_message(self):
        """
        Terminates the connection with the server.
        """
        now = datetime.datetime.now()
        print(f'[{now:%Y-%m-%d %H:%M:%S}] Client disconnected')
        self._conn.close()

    def send_message(self, message):
        """
        Sends data to the connected socket.

        Args:
            message ([str]): message to send
        
        Ensures: the message is sent to the connected socket.
        """
        msg_bytes = pickle.dumps(message, -1)
        size = struct.pack('!i', len(msg_bytes))

        self._conn.sendall(size)
        self._conn.sendall(msg_bytes)