const int MUTED_LED = 13;
const int TALKING_LED = 12;

bool first_contact = false;
bool muted;

void setup() {
  pinMode(MUTED_LED, OUTPUT);
  pinMode(TALKING_LED, OUTPUT);

  //digitalWrite(13, LOW);
  //digitalWrite(12, LOW);
  
  Serial.begin(115200);
}

void loop() {
  if(Serial.available() > 0) {
    if (!first_contact)
      first_contact = true;
      
    char data = Serial.read();
    if (data == 49)
      muted = true;
    else
      muted = false;
  }

  if (first_contact) {
    digitalWrite(MUTED_LED,muted);
    digitalWrite(TALKING_LED,!muted);
  }
  delay(10);
}
