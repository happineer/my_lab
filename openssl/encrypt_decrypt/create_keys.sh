#/bin/bash -e

# 개인 키 생성
openssl genpkey -algorithm RSA -out private.key
echo "[OPENSSL] private.key is generated"

# 공개 키 추출
openssl rsa -pubout -in private.key -out public.key
echo "[OPENSSL] public.key is generated"


