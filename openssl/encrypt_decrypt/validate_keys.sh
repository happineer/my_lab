#!/bin/bash -e

PRI_KEY=$1
PUB_KEY=$2

if [ -z "$PRI_KEY" ]; then
    #openssl genpkey -algorithm RSA -out private.key
    PRI_KEY=private.key
    if [ ! -e "$PRI_KEY" ]; then
        echo "[Error] $PRI_KEY is not exist"
        echo "        you can create a pair of keys by executing -> ./create_keys.sh"
        exit -1
    fi
fi

if [ -z "$PUB_KEY" ]; then
    #openssl rsa -pubout -in private.key -out public.key
    PUB_KEY=public.key
    if [ ! -e "$PUB_KEY" ]; then
        echo "[Error] $PUB_KEY is not exist"
        echo "        you can create a pair of keys by executing -> ./create_keys.sh"
        exit -1
    fi
fi

echo "[1] Random data is generated"
openssl rand -out random_data.bin 32

echo "[2] sign to the random data by 'private.key'"
#openssl pkeyutl -sign -inkey private.key -in random_data.bin -out signature.bin
openssl dgst -sha256 -sign private.key -out signature.bin random_data.bin


echo "[3] check to verify the signature(created by private.key) by 'public.key'"
#openssl pkeyutl -verify -pubin -inkey public.key -in signature.bin -sigfile random_data.bin
openssl dgst -sha256 -verify public.key -signature signature.bin random_data.bin


