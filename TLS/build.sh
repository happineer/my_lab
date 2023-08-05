#!/bin/bash -e

echo "[OPENSSL] start building sever&client"
g++ -o server server.cpp -lssl -lcrypto
g++ -o client client.cpp -lssl -lcrypto
echo "[OPENSSL] build done!"

