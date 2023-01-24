String data[7][2] = {
 {"32.81783914887026", "39.93913214184303"},
 {"32.817918113638626", "39.93906081551407"},
 {"32.817988424734864", "39.938991977243006"},
 {"32.81805981753877", "39.93902681107568"},
 {"32.81791486851202", "39.93916282872868"},
 {"32.81784239399809", "39.9391329712183"},
 {"32.81796138200497", "39.93908154991976"}
};
void setup() {
  // Set the baud rate for serial communication
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i <= 6; i++) {
    // Send the current number
    Serial.print(i);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    // Send the current number
    Serial.print(data[i][0]);
    Serial.print(",");
    Serial.println(data[i][1]);
    // Wait for 1 second
    delay(1000);
  }
}
