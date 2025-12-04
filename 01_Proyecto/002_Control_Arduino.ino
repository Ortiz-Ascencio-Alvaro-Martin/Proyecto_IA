// Pines para el driver A4988
#define STEP_PIN 2
#define DIR_PIN 3

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'A') {
      digitalWrite(DIR_PIN, HIGH); // Dirección 1
      moverMotor(200); // 200 pasos
    } else if (command == 'B') {
      digitalWrite(DIR_PIN, LOW); // Dirección 2
      moverMotor(200); // 200 pasos
    }
  }
}

void moverMotor(int pasos) {
  for (int i = 0; i < pasos; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(800);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(800);
  }
}