# The MIT License (MIT)
# Copyright (c) 2019 Shubhadeep Banerjee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import socket
import sys
import logging
from logging.handlers import RotatingFileHandler
import threading

# define global variables
# timeout to close an idle socket, 0 means no timeout (in seconds)
SOCKET_TIMEOUT = 0
LOGGER_SIZE = 1024 * 1000  # size of individual log file (in Bytes)
LOGGER_BACKUP_COUNT = 10  # no of log backups after the current log file is full

# setup the logger
logger = logging.getLogger('EchoServerLogger')
logger.setLevel(logging.INFO)
logger.propagate = False
hdlr = RotatingFileHandler(
    'server.log', maxBytes=LOGGER_SIZE, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


def log(message):
    """global log method
    """
    print(message)
    logger.info(message)


class SocketServer:
    HOST = ''
    PORT = 0
    s = None

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    def startServer(self):
        """starts the socket server
        """
        log("Opening socket on {0}:{1}".format(self.HOST, self.PORT))
        try:
            s = socket.socket()
            s.bind((self.HOST, self.PORT))
        except socket.error as msg:
            s = None
        try:
            s.listen(5)
            log("Socket is listening on {0}:{1}, timeout {2} sec".format(
                self.HOST, self.PORT, SOCKET_TIMEOUT))
        except:
            if s is not None:
                s.close()
            s = None
        # if socket is not open, exit the program
        if s is None:
            log('Could not open socket')
            sys.exit(1)
        # otherwise run a while loop where we accept an incoming connection
        # and hand it over to the socket handler
        else:
            while True:
                try:
                    sock, addr = s.accept()
                    # create a handler and start the same
                    handler = SocketHandler(sock, addr)
                    handler.start()
                except:
                    break
            log('Program terminated, closing socket!')
            s.close()


class SocketHandler:
    def __init__(self, socket, addr):
        self.socket = socket
        # set the timeout if the timeout is set greater than '0'
        if (SOCKET_TIMEOUT > 0):
            self.socket.settimeout(SOCKET_TIMEOUT)
        self.addr = addr
        self.open = True

    def start(self):
        """creates a thread and starts the handler
        """
        t1 = threading.Thread(target=self.handle, args=[])
        t1.daemon = True
        t1.start()

    def handle(self):
        """Handles a socket client
        """
        # read the socket until the socket is open
        while self.open:
            try:
                # read bytes from socket
                data = self.socket.recv(1024)
                # convert the bytes to readable string
                # here we are using utf-8, but anything character set can be used
                dataStr = data.decode('utf-8')
            except:
                self.open = False
                continue
            if len(dataStr) > 0:
                # if we recive some data, we log and echo back the data
                log('Data from {0} - {1}'.format(self.addr, dataStr))
                # before sending the data we need to encode it back to bytes
                self.socket.send(dataStr.encode())
            elif len(data) == 0:
                # if the data stream is eampty, means the socket is closed
                self.socket.close()
        log('Closed {0}'.format(self.addr))


if __name__ == '__main__':
    # 0.0.0.0 as host ip means it will receive socket connecting from all IPs
    # we can put a specific IP to whitelist the clients
    server = SocketServer('0.0.0.0', 6060)
    server.startServer()
