# Python Socket Echo Client & Server
Simple socket server and client written in python. No extra libraries are needed to run the programs. 

## server.py
This file contains the code of socket server. This code uses multi-threading and can be used in a production server.

## client.py
This file contains the code of a simple socket client. This code is pretty basic but shows all the capabilities of a socket client.

## Compatibility
Both of the client and server is compatible with Python 3 (3.5 and above). This program does not use Python asyncio, it uses the 'socket' library which comes built-in with Python. with little tweaks both can be run on Python 2, but that is not recommended as Python 2 will be expiring soon (in 2020).
