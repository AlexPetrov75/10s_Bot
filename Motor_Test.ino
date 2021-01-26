const int IN1=5;
const int IN2=4;
const int ENA=6;

const int IN3=8;
const int IN4=7;
const int ENB=9;

char incomingByte = 0;
char state = 0;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  Serial.begin(9600); //open serial port
  Serial.println("Press 1, 2, or 3 for fun.");
}

void loop() {
  //Motor1_Break();
  //Motor2_Break();
  //delay(100);
  //Motor1_Forward(50);
  
//  while(1){
//    if(Serial.available() > 0){
//      incomingByte = Serial.read();
//      if(incomingByte != '\n'){
//        Serial.print("I recieved: ");
//        Serial.println(incomingByte);
//        Serial.println("Here");
//        state = incomingByte;
//      }
//      break;
//    }
//    else{
//      continue;
//    }
//  }
//  Serial.println(state);
//  

  
  //example of slowly stepping up
  for(int i=0; i < 100; i++){
    Motor1_Forward(i);
    delay(100);
  }

  //example of slowly stepping down
  for(int j=100; j > 0; j--){
    Motor1_Forward(j);
    delay(100);
  }
  Motor2_Break();
  delay(1000);

  for(int i=0; i < 100; i++){
    Motor1_Backwards(i);
    delay(100);
  }

  //example of slowly stepping down
  for(int j=100; j > 0; j--){
    Motor1_Backwards(j);
    delay(100);
  }
  Motor2_Break();
  delay(1000);
  //Motor2_Forward(50);
  //delay(2000);
  //Motor1_Break();
  //Motor2_Break();
  //delay(100);
  //Motor1_Backwards(255);
  //Motor2_Backwards(50);
  //delay(1000);

}


//Max Speed depends on PWM form 0-255(min-max)
//Can add map later to make it 0-100
void Motor1_Forward(int Speed){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, Speed);
}

void Motor1_Backwards(int Speed){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, Speed);
}

void Motor1_Break(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void Motor2_Forward(int Speed){
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, Speed);
}

void Motor2_Backwards(int Speed){
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, Speed);
}

void Motor2_Break(){
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
