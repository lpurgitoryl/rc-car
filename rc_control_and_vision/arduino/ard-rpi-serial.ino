// assign pin num
// steering pins
int ena = 11; // PWM
int in1 = 10;
int in2 = 9;


// forward/reverse
int enb = 7; // PWM
int in3 = 6;
int in4 = 5;


// duration for output
int time = 100;
// initial command
int command = 0;

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(ena, OUTPUT);

  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enb, OUTPUT);
  

  Serial.begin(115200);
}

void loop() {
  //receive command
  if (Serial.available() > 0){
    command = Serial.read();
    Serial.print(command);
    Serial.print("\n");
    Serial.print("\n");
    command = command;
  }
  else{
    reset();
    // command = 0;
  }
   send_command(command,time);
}

void right(int time){
 digitalWrite(ena, HIGH);
 digitalWrite(in1, LOW);
 digitalWrite(in2, HIGH);
  
  delay(time);
}

void left(int time){

 digitalWrite(ena, HIGH);
 digitalWrite(in1, HIGH);
 digitalWrite(in2, LOW);
 
 delay(time);
}

void forward(int time){
 
 digitalWrite(enb, HIGH);
 digitalWrite(in3, HIGH);
 digitalWrite(in4, LOW);
 
  delay(time);
}

void reverse(int time){
 digitalWrite(enb, HIGH);
 digitalWrite(in3, LOW);
 digitalWrite(in4, HIGH);
 
  delay(time);
}

void forward_right(int time){
 digitalWrite(enb, HIGH);
 digitalWrite(in3, HIGH);
 digitalWrite(in4, LOW);

 digitalWrite(ena, HIGH);
 digitalWrite(in1, LOW);
 digitalWrite(in2, HIGH);
 
 
  delay(time);
}

void reverse_right(int time){
 digitalWrite(enb, HIGH);
 digitalWrite(in3, LOW);
 digitalWrite(in4, HIGH);

 digitalWrite(ena, HIGH);
 digitalWrite(in1, LOW);
 digitalWrite(in2, HIGH);
  delay(time);
}

void forward_left(int time){
 digitalWrite(enb, HIGH);
 digitalWrite(in3, HIGH);
 digitalWrite(in4, LOW);

 digitalWrite(ena, HIGH);
 digitalWrite(in1, HIGH);
 digitalWrite(in2, LOW);

 
 
  delay(time);
}

void reverse_left(int time){
 digitalWrite(enb, HIGH);
 digitalWrite(in3, LOW);
 digitalWrite(in4, HIGH);

 digitalWrite(ena, HIGH);
 digitalWrite(in1, HIGH);
 digitalWrite(in2, LOW);
 
  delay(time);
}

void reset(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(ena, LOW);

  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  digitalWrite(enb, LOW);
}

void send_command(int command, int time){
  switch (command){

     //reset command
     case 0: reset(); break;

     // single command
     case 1: forward(time); break;
     case 2: reverse(time); break;
     case 3: right(time); break;
     case 4: left(time); break;

     //combination command
     case 6: forward_right(time); break;
     case 7: forward_left(time); break;
     case 8: reverse_right(time); break;
     case 9: reverse_left(time); break;

     default: Serial.print("Inalid Command\n");
    }
}
