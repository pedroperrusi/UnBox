""" Classe responsável por receber cada cliente em uma Thread """

import socket
import threading

import database

class ClientThread(threading.Thread):
    """ Classe ClientThread

    Responsável por receber um novo cliente em uma thread independente.

    Attributes:
        clientAddress:
        clientsocket:
    """

    def __init__(self,clientAddress,clientsocket):
        """ Contrutor da classe. """
        threading.Thread.__init__(self)
        self.client_socket = clientsocket
        self.client_address = clientAddress
        print ("New connection added: ", self.client_address)

    def run(self):
        """ Main thread function

        Called after thread is started: ie. thread.start().
        Recieves operation commands through socket and performs them.
        """

        print ("Connection from : ", self.client_address)
        msg = ''
        while True:
            msg = self.recieve_text()
            if msg=='bye':
                print ('User ', self.username, ' at ', self.client_address , ' disconnected...')
                break
            # Processes an operation commands (comma separated) -----------------------------
            split_msg = msg.split(',')
            if split_msg[0] == 'Log-in request':
                self.log_in_request(split_msg)
            if split_msg[0] == 'Register request':
                self.register_request(split_msg)

    def send_text(self, msg):
        """ Sends text message through socket connection """
        self.client_socket.send(bytes(msg,'UTF-8'))

    def recieve_text(self):
        """ Returns text message recieved by the socket """
        data = self.client_socket.recv(2048)
        return data.decode()

    def log_in_request(self, message):
        """ Processes a login request recieved for the client.

        arguments:
            message: expected message is an array on the following format:
                ['Log-in Request', Username, Password]
        """
        print(message[0])
        username = message[1]
        password = message[2]
        print('\t Username: {}'.format(username))
        print('\t Password: {}'.format(password))
        user_exists, password_correct = database.authenticate_user(username, password)

        if user_exists and password_correct:
            print('User authenticated')
            self.send_text('Found')
        elif user_exists:
            print('Authentication failure')
            print ('Password incorrect')
            self.send_text('Password incorrect')
        else:
            print('Authentication failure')
            print('User doesnt exist')
            self.send_text('Not found')

        self.username, self.password = username, password

    def register_request(self, message):
        """ Process an registration request for the client

        arguments:
            message: expected message is an array on the following format:
                ['Register request', Username, Password]
        """
        print(message[0])
        username = message[1]
        password = message[2]
        print('Username: {}'.format(username))
        print('Password: {}'.format(password))
        database.register_user(username, password)
        self.send_text('Created')
