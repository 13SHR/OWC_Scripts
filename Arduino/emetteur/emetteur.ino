int led = 12;
int pause = 500;

void setup()
{
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop()
{
  while (Serial.available() != 0)
  {
    char c = Serial.read();
    if (c != '\n') {
      Serial.println("-----\nDébut émission\n-----\n");
      
      digitalWrite(led, HIGH); // Indication de début d'émission
      delay(pause);
      
      for (int i = 7; i >= 0; i--) {
        int b = (c >> i) % 2;
        Serial.print("b :");
        Serial.println(b);
        digitalWrite(led, b ? HIGH : LOW);
        delay(pause);
      }

      Serial.println("-----\nEmission effectuée\n-----\n");
    }
  }

  digitalWrite(led, LOW);
  delay(1);
}
