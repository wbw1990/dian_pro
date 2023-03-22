#!/bin/bash

# python3 -u /runtime/index.py &
# python3 -u /runtime/lib/ws_server.py 
python3 -u /runtime/lib/bluetooth_client.py &
python3 -u /runtime/index_init.py