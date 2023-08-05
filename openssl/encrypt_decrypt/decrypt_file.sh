#!/bin/bash -e

IN_FILENAME=$1
PRI_KEY=$2
OUT_FILENAME=$3
if [ -z "$IN_FILENAME" ]; then
    echo "[Error] input the argument like the below"
    echo "  $ "$0" enc_out.txt [private.key] [enc_out.txt]"
    exit 1
fi

if [ -z "$PRI_KEY" ]; then
    PRI_KEY=private.key
fi

if [ -z "$OUT_FILENAME" ]; then
    OUT_FILENAME=dec_out.txt
fi

openssl pkeyutl -decrypt -inkey ${PRI_KEY} -in ${IN_FILENAME} -out ${OUT_FILENAME}
echo "[OPENSSL] $OUT_FILENAME is created"

