#!/usr/bin/python3

import eventlet

# 이벤트 객체 생성
event = eventlet.Event()

# 이벤트를 처리할 함수
def handle_event(name):
    print(f"{name} 이벤트 처리 시작")
    with eventlet.Timeout(10, False):  # 2초 Timeout 설정, False는 Timeout 발생 시 False를 반환하도록 합니다.
        print("[SJH] handle_event started")
        event.wait()  # 이벤트가 발생할 때까지 최대 2초까지 기다립니다.
    if not event.ready():
        print(f"{name} 이벤트 처리 Timeout 발생")
    else:
        print(f"{name} 이벤트 처리 완료")

# 스레드 생성
thread1 = eventlet.spawn(handle_event, "스레드 1")
thread2 = eventlet.spawn(handle_event, "스레드 2")

# 이벤트 발생시키기
# 여기서는 1초 후에 이벤트를 발생시킵니다.
eventlet.spawn_after(3, event.send)

# 모든 스레드들이 처리를 완료할 때까지 기다립니다.
thread1.wait()
thread2.wait()
