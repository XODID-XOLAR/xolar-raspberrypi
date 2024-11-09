from gpiozero import Motor
import time

motor1 = Motor(forward=20, backward=21)
motor2 = Motor(forward=23, backward=24)
motor3 = Motor(forward=27, backward=17)
motor4 = Motor(forward=22, backward=6)

# 모두 내리기
motor1.backward()
motor2.backward()
motor3.backward()
motor4.backward()
time.sleep(60)
motor1.stop()
motor2.stop()
motor3.stop()
motor4.stop()

# 동쪽 바라보기
motor1.forward(1.0)
motor2.forward(1.0)
time.sleep(80)
motor1.stop()
motor2.stop()

    
# 남쪽 바라보기
motor1.backward(0.5)
motor3.forward(1.0)
motor4.forward(0.5)
time.sleep(80)
motor1.stop()
motor2.stop()
motor3.stop()
motor4.stop()

# 서쪽 바라보기
motor1.backward(0.5)
motor2.backward(1.0)
motor3.forward(0.6)
motor4.forward(1.0)
time.sleep(80)
motor1.stop()
motor2.stop()
motor3.stop()
motor4.stop()
