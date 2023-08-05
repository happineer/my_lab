#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCKET_PATH "/tmp/uds_socket"
#define BUFFER_SIZE 1024

int main() {
    int server_socket, client_socket;
    struct sockaddr_un server_addr, client_addr;
    char buffer[BUFFER_SIZE];

    // UDS 소켓 생성
    server_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // 서버 소켓 주소 설정
    memset(&server_addr, 0, sizeof(struct sockaddr_un));
    server_addr.sun_family = AF_UNIX;
    strncpy(server_addr.sun_path, SOCKET_PATH, sizeof(server_addr.sun_path) - 1);

    // 기존에 같은 경로명의 소켓 파일이 있다면 삭제
    unlink(SOCKET_PATH);

    // UDS 소켓 바인딩
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(struct sockaddr_un)) < 0) {
        perror("bind");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    // 클라이언트 연결 대기
    if (listen(server_socket, 1) < 0) {
        perror("listen");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("서버가 시작되었습니다. 클라이언트의 접속을 기다립니다...\n");

    // 클라이언트 연결 수락
    socklen_t client_addr_len = sizeof(struct sockaddr_un);
    client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
    if (client_socket < 0) {
        perror("accept");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("클라이언트가 연결되었습니다.\n");

    // 클라이언트로부터 데이터 수신 후 출력
    ssize_t received_bytes;
    while ((received_bytes = recv(client_socket, buffer, sizeof(buffer), 0)) > 0) {
        buffer[received_bytes] = '\0';
        printf("클라이언트로부터 수신된 데이터: %s\n", buffer);
    }

    // 연결 종료 및 소켓 제거
    close(client_socket);
    close(server_socket);
    unlink(SOCKET_PATH);

    return 0;
}
