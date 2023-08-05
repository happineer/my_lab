#!/bin/bash -e

echo "[UDS-SOCKET] start building sever&client"
g++ server.cpp -o server
g++ client.cpp -o client

echo "[UDS-SOCKET] build done!"

