
int v = 0;
int sign = 1;

#include <Stepper.h>
#include <Servo.h>
// write a,b for steppers
Stepper motor1 = Stepper(200, 4,5, 6,7);
Stepper motor2 = Stepper(200, 10,11,12,13);
Servo myservo;
int rpm = 60;

void setup() {

    Serial.begin(38400); 
    Serial.println("Stepper test!");
    motor1.setSpeed(rpm);  // rpm  
    motor2.setSpeed(rpm);
    myservo.attach(3);
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
      case 'c':
         move('c', v, sign);
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

void move(char ch, int steps, int sign) {

  switch(ch) {

    case 'a':
      motor1.step(steps*sign);
    break;
    case 'b':
      motor2.step(steps* sign);
    break;
    case 'c':
      myservo.write(steps);
    break;
    
    
  }
}

