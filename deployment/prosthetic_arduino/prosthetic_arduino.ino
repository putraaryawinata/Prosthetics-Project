#include <Wire.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
String command;
int sudut = 0; // variable to store the servo position

int pin0, pin1, pin2, pin3, pin4, pin5, pin6;
String string_hasil = "";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  myservo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  string_hasil = "";
  pin0 = analogRead(A0);
  string_hasil += "A0 " + String(pin0) + " ";
  pin1 = analogRead(A1);
  string_hasil += "A1 " + String(pin1) + " ";
  pin2 = analogRead(A2);
  string_hasil += "A2 " + String(pin2) + " ";
  pin3 = analogRead(A3);
  string_hasil += "A3 " + String(pin3) + " ";
  pin4 = analogRead(A4);
  string_hasil += "A4 " + String(pin4) + " ";
  pin5 = analogRead(A5);
  string_hasil += "A5 " + String(pin5);
  Serial.println(string_hasil);

  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
    sudut = command.toInt();
    Serial.println(sudut);
    //myservo.write(sudut);
  }
  myservo.write(sudut);

  delay(10);
}
