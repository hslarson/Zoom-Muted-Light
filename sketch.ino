const int MUTED_LED = 13;
const int TALKING_LED = 12;

bool first_contact = false;
bool muted;

void setup() {
  pinMode(MUTED_LED, OUTPUT);
  pinMode(TALKING_LED, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  if(Serial.available() > 0) {
    if (!first_contact)
      first_contact = true;
      
    char data = Serial.read();
    //Got ASCII '0' (talking)
    if (data == 48)
      muted = false;

    //Got ASCII '1' (Muted)
    else if (data == 49)
      muted = true;

    //Got ASCII '2' (Turn Off)
    else if (data == 50){
      digitalWrite(MUTED_LED, LOW);
      digitalWrite(TALKING_LED, LOW);
      first_contact = false;
    }
  }

  if (first_contact) {
    digitalWrite(MUTED_LED,muted);
    digitalWrite(TALKING_LED,!muted);
  }

  delay(10);
}
