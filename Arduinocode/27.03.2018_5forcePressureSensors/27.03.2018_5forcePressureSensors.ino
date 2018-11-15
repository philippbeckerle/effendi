// this code reads data from 5 froce pressure sensors and writes them to the serial port. Additionally it is possible to control a LED by writing to the serial port.

void setup() {
  Serial.begin(9600);
}

void loop() {  //Reading analog inputs from FSRs and sending them to Python
  analogRead(0);
  delay (2);
  int pressureValue0 = analogRead(0);

  analogRead(1); //trashanalogreadings due to impedance when Arduino switches to multiplexer readout.
  delay (2);     //Reading out each port twice reduces error that can occurr between the analog ports.
  int pressureValue1 = analogRead(1);

  analogRead(2);
  delay(2);
  int pressureValue2 = analogRead(2);

  analogRead(3);
  delay(2);
  int pressureValue3 = analogRead(3);

  analogRead(4);
  delay(2);
  int pressureValue4 = analogRead(4);

  Serial.print(pressureValue0);
  Serial.print(";");
  Serial.print(pressureValue1);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.print(";");
  Serial.print(pressureValue3);
  Serial.print(";");
  Serial.print(pressureValue4);
  Serial.println(";");

  delay (100);
}
