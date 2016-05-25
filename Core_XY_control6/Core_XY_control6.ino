
int v = 0;
int sign = 1;

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>
#define SERVOPIN 9
#define TOUCHDOWN_PIN 8
#define X_LIMIT_PIN 2
#define Y_LIMIT_PIN 3

// write a,b for steppers
AccelStepper stepper1(AccelStepper::FULL4WIRE, 4, 5, 6, 7);
AccelStepper stepper2(AccelStepper::FULL4WIRE, A5, A4, A3, A2);

long positions[2]= {0,0};

// Up to 10 steppers can be handled as a group by MultiStepper
MultiStepper steppers;
Servo myservo;


void setup() {

    Serial.begin(38400);
    Serial.print("LET'S PRINT BABAAAAH!\n"); //This is important for some reason?
    stepper1.setMaxSpeed(100);
    stepper2.setMaxSpeed(100);
    myservo.attach(SERVOPIN);
      // Then give them to MultiStepper to manage
    steppers.addStepper(stepper1);
    steppers.addStepper(stepper2);
    pinMode(TOUCHDOWN_PIN, INPUT_PULLUP);
    pinMode(X_LIMIT_PIN, INPUT_PULLUP);
    pinMode(Y_LIMIT_PIN, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
   if ( Serial.available()) {
    char ch = Serial.read();

    switch(ch) {
      case '0'...'9':
      //Pretty goddamn clever right here. Not mine.
        v = v * 10 + ch - '0';
      break;
      case '-':
      //Pretty goddamn clever right here. This time ours.
        sign *= -1;
        //Serial.println("NEGATE!");
      break;
      case 'a':
        move('a', v, sign);
        resetV();
      break;
      case 'b':
        move('b', v, sign);
        resetV();
        break;
      case 'c': // Move
         move('c', v, sign);
         resetV();
         break;
      case 's': // Set Speed
         stepper1.setMaxSpeed(v);
         stepper2.setMaxSpeed(v);
         resetV();
         break;
      case 'r':
        resetCoordinates();
        resetV();
        break;
      case 'h':
        touchdown();
        resetV();
        break;
      case 'z':
        homeCoords();
        resetV();
        break;
      case 'x': // Execute action
         steppers.moveTo(positions);
         steppers.runSpeedToPosition();
         Serial.print("Ready\n");
         resetV();
         break;

      default:
        Serial.write("...the fuck is that?");
        resetV();
        break;
    }
   }
}

void resetV() {
  sign = 1;
  v = 0;
}

void homeCoords() {
  Serial.println("homing");
  bool x_home = false;
  bool y_home = false;
  y_home = (digitalRead(Y_LIMIT_PIN) == 0);
  while (!y_home){
    positions[0] -= 1;
    positions[1] += 1;
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
    y_home = (digitalRead(Y_LIMIT_PIN) == 0);
  }


  x_home = (digitalRead(X_LIMIT_PIN) == 0);
  while (!x_home){
    positions[0] -= 1;
    positions[1] -= 1;
    steppers.moveTo(positions);
    steppers.runSpeedToPosition();
    x_home = (digitalRead(X_LIMIT_PIN) == 0);
  }

  resetCoordinates();
}

void resetCoordinates() {
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);
}

void touchdown(){
   int angle = 90;
    myservo.write(angle);
    delay(10);
  while(digitalRead(TOUCHDOWN_PIN) == 1 && angle > 0){
    angle--;
    myservo.write(angle);
    delay(50);
    //Serial.println(digitalRead(TOUCHDOWN_PIN));
  }
  Serial.println(angle);
  myservo.write(90);
}

void move(char ch, int steps, int sign) {

  switch(ch) {

    case 'a':
      positions[0]=long(steps*sign);
    break;
    case 'b':
      positions[1]=long(steps*sign);
    break;
    case 'c':
      myservo.write(steps);
    break;


  }
}
