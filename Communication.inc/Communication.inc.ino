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

void loop() {
  // put your main code here, to run repeatedly:

  if (stringComplete) {
    sendMessage();
    stringComplete = false;
    inputString = "";
  }

  if (Serial.available() > 0) serialEvent();

  delay(10);

}

void sendMessage(){
  char buffer[50];
  sprintf(buffer, "Hello there");
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
