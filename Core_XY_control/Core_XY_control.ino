
#include <AFMotor.h>
int v = 0;
int sign = 1;

// Connect a stepper motor with 48 steps per revolution (7.5 degree)
// to motor port #2 (M3 and M4)
AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

void setup() {
  // put your setup code here, to run once:

    Serial.begin(38400);           // set up Serial library at 9600 bps
    Serial.println("Stepper test!");

    motor1.setSpeed(200);  // 10 rpm  
    motor2.setSpeed(200);
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
      int dir;
    if(sign <= 0){
      //Serial.println("BACKWARD!");
      dir = BACKWARD;
    }
    else{
        dir = FORWARD;
     }
  switch(ch) {

    case 'a':
      motor1.step(steps, dir, MICROSTEP);
    break;
    case 'b':
      motor2.step(steps, dir, MICROSTEP);
    break;
    
  }
}
