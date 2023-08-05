#!/bin/bash -e

IN_FILENAME=$1
PUB_KEY=$2
OUT_FILENAME=$3

if [ -z "$IN_FILENAME" ]; then
    echo "[Error] input the argument like the below"
    echo "  $ "$0" orig.txt [public.key] [enc_out.txt]"
    exit 1
fi

if [ -z "$PUB_KEY" ]; then
    PUB_KEY=public.key
fi

if [ -z "$OUT_FILENAME" ]; then
    OUT_FILENAME=enc_out.txt
fi

openssl pkeyutl -encrypt -pubin -inkey ${PUB_KEY} -in ${IN_FILENAME} -out ${OUT_FILENAME}
echo "[OPENSSL] $OUT_FILENAME is created"

