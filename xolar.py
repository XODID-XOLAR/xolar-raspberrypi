import paho.mqtt.client as mqtt
import time
import json
from gpiozero import Motor

# GPIO 핀 설정 (모터 제어 핀 지정)
motor1 = Motor(forward=20, backward=21)
motor2 = Motor(forward=23, backward=24)

# MQTT 브로커 및 연결 설정
BROKER = "{AWS IoT EndPoint}"  # AWS IoT > 연결 > 도메인 구성 > iot:Data-ATS
PORT = 8883
TOPIC = "$aws/things/{사물 이름}/shadow/update"

# 인증서 파일 경로 설정
CA_PATH = "/home/pi/certificates/AmazonRootCA1.pem"
CERT_PATH = "/home/pi/certificates/certificate.pem.crt"
KEY_PATH = "/home/pi/certificates/private.pem.key"

# MQTT 연결 콜백 함수 정의
def on_connect(client, userdata, flags, rc):
    print("MQTT Connect Success, Code:", rc)  # 연결 성공 메시지 출력
    client.subscribe(TOPIC)  # 지정된 토픽 구독 시작

# MQTT 메시지 수신 콜백 함수 정의
def on_message(client, userdata, msg):
    payload = msg.payload.decode()  # 수신된 메시지 디코딩
    print("Received Message:", payload)  # 수신된 메시지 출력

    # 수신된 메시지를 JSON으로 파싱하여 비상 상태 추출
    data = json.loads(payload)
    emergency_status = data.get("state", {}).get("reported", {}).get("status")

    # 비상 상태에 따른 모터 동작
    if emergency_status == "STRONG_WIND":
        # 강풍 비상 상태
        print("Strong-Wind")  
        motor1.forward()
        motor2.forward()
        time.sleep(30)
        motor1.stop()
        motor2.stop()
    elif emergency_status == "HEAVY_SNOW":
        # 폭설 비상 상태
        print("Heavy-Snow")  
        motor1.backward()
        motor2.backward()
        time.sleep(30)
        motor1.stop()
        motor2.stop()
    else:
        # 정상 상태 - 추후 태양 추적 알고리즘을 사용해 태양을 따라 움직이도록 설정할 예정
        print("Normal")

# MQTT 클라이언트 설정 및 실행
client = mqtt.Client()
client.tls_set(CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)  # 보안 인증 설정
client.on_connect = on_connect  # 연결 콜백 함수 설정
client.on_message = on_message  # 메시지 수신 콜백 함수 설정

# MQTT 브로커에 연결하고, 무한 루프로 메시지 수신 대기
client.connect(BROKER, PORT)
client.loop_forever()
