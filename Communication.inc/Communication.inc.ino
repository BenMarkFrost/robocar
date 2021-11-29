#define ENB 6 
#define IN3 9
#define IN4 11
#define ENA 5 
#define IN1 7
#define IN2 8

boolean stringComplete = false;
String inputString = "";

void setup() {
  pinMode(IN1, OUTPUT);   //set IO pin mode OUTPUT
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); //set IO pin mode OUTPUT
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  digitalWrite(ENB, HIGH);  //Enable right motor    
  digitalWrite(ENA, HIGH);//Enable left motor    

  Serial.begin(9600);
  while(!Serial){
    ;
  }

}

void turnLeft(){
  digitalWrite(IN3, LOW);      
  digitalWrite(IN4, HIGH);//Right wheel turning forwards
  delay(200);
  digitalWrite(IN3, LOW);      
  digitalWrite(IN4, LOW); //Right wheel stopped
}

void turnRight(){
  digitalWrite(IN1, HIGH);      
  digitalWrite(IN2, LOW); //Left wheel turning forwards
  delay(200);             //delay 500ms
  digitalWrite(IN1, LOW);      
  digitalWrite(IN2, LOW); //Left wheel stoped
}

void moveForward(){
  digitalWrite(IN1, HIGH);      
  digitalWrite(IN2, LOW); 
  digitalWrite(IN3, LOW);      
  digitalWrite(IN4, HIGH);  //go forward
  delay(200);
  digitalWrite(IN1, LOW);      
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);      
  digitalWrite(IN4, LOW);   //stop
}

void loop() {
  // put your main code here, to run repeatedly:

  if (stringComplete) {

    inputString = inputString.substring(0,3);
    
    if (inputString == "fwd"){
      sendMessage("moving forward");
      moveForward();
    } else{
      sendMessage("no command");
    }

    stringComplete = false;
    inputString = "";
  }

  if (Serial.available() > 0) serialEvent();

  delay(10);

}

void sendMessage(String message){
  char buffer[50];
  sprintf(buffer, message.c_str());
  Serial.println(buffer);
}


void serialEvent(){
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
