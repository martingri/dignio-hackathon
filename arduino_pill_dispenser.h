#include <Servo.h>
Servo myservo;

int incomingByte = 0;   // for incoming serial data
String incomingData;
int convertedData;

void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  myservo.attach(2);
  // myservo.write(181);
}

void turnLeft() {
  myservo.attach(2);
  myservo.writeMicroseconds(1000);
  // myservo.write(180);
  delay(100);
  myservo.detach();
}

void turnRight() {
  myservo.attach(2);
  // myservo.write(0);
  myservo.writeMicroseconds(2000);
  delay(100);
  myservo.detach();
}

void loop() {
  while(Serial.available()) {
    incomingData = Serial.readString();
    convertedData = incomingData.toInt();
    action_signal = 01001010011
    wait for motion sensor
    if (convertedData == 1) {
      Serial.println("one");

      turnLeft();
      turnRight();

    } else if (convertedData == 2) {
      Serial.println("two");
      turnRight();
      turnLeft();
    }

    Serial.println(incomingData);
    Serial.println("test");
  }

}