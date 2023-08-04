#!/usr/bin/python3

import eventlet

# 이벤트 객체 생성
event = eventlet.Event()

# 이벤트를 처리할 함수
def handle_event(name):
    print(f"{name} 이벤트 처리 시작")
    event.wait()  # 이벤트가 발생할 때까지 기다립니다.
    print(f"{name} 이벤트 처리 완료")

# 스레드 생성
thread1 = eventlet.spawn(handle_event, "스레드 1")
thread2 = eventlet.spawn(handle_event, "스레드 2")

# 스레드들이 이벤트를 기다리고 있으므로, 이벤트를 발생시키면 이벤트를 기다리던 스레드들이 동시에 실행됩니다.
event.send()

# 모든 스레드들이 처리를 완료할 때까지 기다립니다.
thread1.wait()
thread2.wait()
