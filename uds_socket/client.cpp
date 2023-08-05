#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCKET_PATH "/tmp/uds_socket"
#define BUFFER_SIZE 1024

int main() {
    int client_socket;
    struct sockaddr_un server_addr;
    char buffer[BUFFER_SIZE];

    // UDS 소켓 생성
    client_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    if (client_socket < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // 서버 소켓 주소 설정
    memset(&server_addr, 0, sizeof(struct sockaddr_un));
    server_addr.sun_family = AF_UNIX;
    strncpy(server_addr.sun_path, SOCKET_PATH, sizeof(server_addr.sun_path) - 1);

    // 서버에 연결
    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(struct sockaddr_un)) < 0) {
        perror("connect");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    printf("서버에 연결되었습니다. 메시지를 전송합니다...\n");

    // 클라이언트가 보낼 데이터
    const char *message = "Hello, Unix Domain Socket!";

    // 데이터 전송
    if (send(client_socket, message, strlen(message), 0) < 0) {
        perror("send");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    // 연결 종료
    close(client_socket);

    return 0;
}
