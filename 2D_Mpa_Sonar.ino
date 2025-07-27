#include <Arduino.h>
#include <ESP32Servo.h>   // کتابخانه مخصوص ESP32

const int echoPin = 2;
const int trigPin = 4;
const int servoPin = 15;

Servo myServo;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // ⚠️ ESP32 نیاز به این تنظیمات داره:
  myServo.setPeriodHertz(50);         // فرکانس استاندارد سروو
  myServo.attach(servoPin, 500, 2400); // min/max pulse width in microseconds
}

float getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  float distance = duration * 0.034 / 2.0;
  if (distance == 0 || distance > 500) distance = 500.0;
  return distance;
}

void loop() {
  for (int angle = 0; angle <= 180; angle++) {
    myServo.write(angle);
    delay(80);
    float distance = getDistance();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }

  for (int angle = 180; angle >= 0; angle--) {
    myServo.write(angle);
    delay(80);
    float distance = getDistance();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}
