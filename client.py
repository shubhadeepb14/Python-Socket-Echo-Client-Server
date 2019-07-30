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
import time

HOST = 'localhost'  # The server's hostname or IP address
PORT = 6060   # The port used by the server
# timeout to close an idle socket, 0 means no timeout (in seconds)
SOCKET_TIMEOUT = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    if (SOCKET_TIMEOUT > 0):
        s.settimeout(SOCKET_TIMEOUT)
    print("Connected to {0}:{1}".format(HOST, PORT))
    # we will send the timestamp in every 5 seconds
    while True:
        try:
            # send the time after encoding it to bytes
            timeStr = str(time.time())
            s.sendall(timeStr.encode())
            print("Sent {0}".format(timeStr))
            # read the response from the server
            # convert the bytes to readable string
            # here we are using utf-8, but anything character set can be used
            response = s.recv(1024)
            # if the data is empty, that means the server has closed the connection
            if len(response) == 0:
                break
            else:
                print("Received {0}".format(response.decode('utf-8')))
            # wait for 5 seconds
            time.sleep(5)
        except:
            break
    print("Connection closed")
