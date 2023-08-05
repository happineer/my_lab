#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 12345
#define CERT_FILE "client.crt"
#define KEY_FILE "client.key"

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    SSL_CTX *ctx;
    SSL *ssl;
    char buffer[1024];

    // OpenSSL 초기화
    SSL_library_init();
    ctx = SSL_CTX_new(TLSv1_2_client_method());

    // 서버 인증서와 개인 키 로드
    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Error loading client certificate.\n");
        exit(EXIT_FAILURE);
    }
    if (SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Error loading client private key.\n");
        exit(EXIT_FAILURE);
    }

    // 소켓 생성 및 연결
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));

    // SSL 연결 설정
    ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sockfd);
    if (SSL_connect(ssl) <= 0) {
        fprintf(stderr, "Error connecting SSL.\n");
        SSL_free(ssl);
        close(sockfd);
        SSL_CTX_free(ctx);
        exit(EXIT_FAILURE);
    }

    // 서버로 데이터 송신 및 수신
    SSL_write(ssl, "Hello from client!", strlen("Hello from client!"));
    SSL_read(ssl, buffer, sizeof(buffer) - 1);
    printf("Received from server: %s\n", buffer);

    // 연결 종료
    SSL_free(ssl);
    close(sockfd);
    SSL_CTX_free(ctx);
    return 0;
}
