import paho.mqtt.client as mqtt
import time
import json

from gpiozero import Motor

# GPIO 핀 설정 (모터 제어 핀 지정)
motor1 = Motor(forward=20, backward=21)
motor2 = Motor(forward=23, backward=24)

motor3 = Motor(forward=27, backward=17)
motor4 = Motor(forward=22, backward=6)

# MQTT 브로커 및 연결 설정
BROKER = "a3p9eizp6emyml-ats.iot.ap-northeast-2.amazonaws.com"  # AWS IoT > 연결 > 도메인 구성 > iot:Data-ATS
PORT = 8883
TOPIC = "$aws/things/aaa/shadow/update"

# 인증서 파일 경로 설정
CA_PATH = "/home/pi/certificates/AmazonRootCA1.pem"
CERT_PATH = "/home/pi/certificates/certificate.pem.crt"
KEY_PATH = "/home/pi/certificates/private.pem.key"

# MQTT 연결 콜백 함수 정의
def on_connect(client, userdata, flags, rc):
    print("MQTT Connect Success, Code:", rc)
    client.subscribe(TOPIC)

# MQTT 메시지 수신 콜백 함수 정의
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Recieved Message:", payload)

    # 수신된 메시지를 JSON으로 파싱하여 비상 상태 추출
    data = json.loads(payload)
    emergency_status = data.get("state", {}).get("reported", {}).get("status")

    # 비상 상태에 따른 모터 동작
    if emergency_status == "STRONG_WIND":
        # 강풍 비상 상태
        print("Strong-Wind")
        motor1.backward(1.0)
        motor2.backward(1.0)
        motor3.backward(1.0)
        motor4.backward(1.0)
        time.sleep(100)
        motor1.stop()
        motor2.stop()
        motor3.stop()
        motor4.stop()
    elif emergency_status == "HEAVY_SNOW":
        # 폭설 비상 상태
        print("Heavy-Snow")
        motor1.backward(1.0)
        motor2.backward(1.0)
        motor3.forward(1.0)
        motor4.forward(1.0)
        time.sleep(100)
        motor1.stop()
        motor2.stop()
        motor3.stop()
        motor4.stop()
    else:
        # 정상 상태 - 추후 태양 추적 알고리즘을 사용해 태양을 따라 움직이도록 설정할 예정
        print("Normal")

# MQTT 클라이언트 설정 및 실행
client = mqtt.Client()
client.tls_set(CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결하고, 무한 루프로 메시지 수신 대기
client.connect(BROKER, PORT)
client.loop_forever()
