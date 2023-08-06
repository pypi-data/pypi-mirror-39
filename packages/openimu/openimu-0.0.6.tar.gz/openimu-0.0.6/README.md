# python-openimu
Python driver for Aceinna OpenIMU Series Inertial Products.  Includes local and cloud file logging, and WebSocket server

### pip install:
pyserial  
tornado  
azure-storage-blob
psutil
pathlib
requests

### openimu.py
This is core driver for OpenIMU.  It can do the following functions:

- automatically discover an OpenIMU connected to serial port  
- log data to local file or azure cloud 
- parse various ouput packets
- read/write and get/set EEPROM fields
- upgrade firmware of device
- run as a thread in websocket server see below

### server.py
Create a web socket server on wss://localhost:8000 that bridges ANS to a locally running openimu serial port driver.  Places openimu driver in a thread

- automatically sends data out on wss://localhost:8000 every 33mS encoding packet as JSON.  
- receives messages via on_message handler from ANS currently messages are - status, start_log, stop_log and cmd.  


### file_storage.py 

These file store parsed packet data to CSV either locally or on Azure cloud.  Uses Azure Python SDK to write to Azure.  

### commands.py

Command Line Interface to access OpenIMU device

### data/ directory

Log files .csv are saved under the directory


