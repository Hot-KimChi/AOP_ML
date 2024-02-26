import socket
import time

# 서버의 호스트와 포트 번호 설정
host = '192.168.10.14'
port = 1023

# 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓 연결 타임아웃 설정 (5초)
sock.settimeout(0.2)

connected = False

while not connected:
    try:
        # 서버에 연결 시도
        sock.connect((host, port))
        connected = True
        print("서버에 연결되었습니다.")

        # 데이터 수신
        data = sock.recv(1024)

        # 수신한 데이터 출력
        print("Received data:", data.decode())

    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다.")
        # 재접속 대기 시간
        time.sleep(5)

    except socket.timeout:
        print("소켓 연결 시간이 초과되었습니다.")

    finally:
        message = "quit"
        sock.sendall(message.encode())

        # 소켓 연결 종료
        sock.close()