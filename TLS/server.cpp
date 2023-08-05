#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

#define SERVER_PORT 12345
#define CERT_FILE "server.crt"
#define KEY_FILE "server.key"

int main() {
    int sockfd, clientfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    SSL_CTX *ctx;
    SSL *ssl;
    char buffer[1024];

    // OpenSSL 초기화
    SSL_library_init();
    ctx = SSL_CTX_new(TLSv1_2_server_method());

    // 서버 인증서와 개인 키 로드
    if (SSL_CTX_use_certificate_file(ctx, CERT_FILE, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Error loading server certificate.\n");
        exit(EXIT_FAILURE);
    }
    if (SSL_CTX_use_PrivateKey_file(ctx, KEY_FILE, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Error loading server private key.\n");
        exit(EXIT_FAILURE);
    }

    // 소켓 생성 및 바인딩
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(sockfd, 5);

    // 클라이언트 연결 대기
    clientfd = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);
    close(sockfd);

    // SSL 연결 설정
    ssl = SSL_new(ctx);
    SSL_set_fd(ssl, clientfd);
    if (SSL_accept(ssl) <= 0) {
        fprintf(stderr, "Error accepting SSL connection.\n");
        SSL_free(ssl);
        close(clientfd);
        SSL_CTX_free(ctx);
        exit(EXIT_FAILURE);
    }

    // 클라이언트로부터 데이터 수신 및 송신
    SSL_read(ssl, buffer, sizeof(buffer) - 1);
    printf("Received from client: %s\n", buffer);
    SSL_write(ssl, "Hello from server!", strlen("Hello from server!"));

    // 연결 종료
    SSL_free(ssl);
    close(clientfd);
    SSL_CTX_free(ctx);
    return 0;
}
