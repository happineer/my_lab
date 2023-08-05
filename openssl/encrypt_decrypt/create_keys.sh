#/bin/bash -e

# 개인 키 생성
openssl genpkey -algorithm RSA -out private.key

# 공개 키 추출
openssl rsa -pubout -in private.key -out public.key
