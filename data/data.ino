String data1 = "33,0,1000,1100,1200,1300,70,2.85,-1.45,-56.45,725.5,1500,1600,1700,1800";

String data2 = "33,01,10001,11001,12001,13001,701,2.851,-1.451,-56.451,725.51,15001,16001,17001,18001";

void setup() {
  // Set the baud rate for serial communication
  Serial.begin(9600);
}

void loop() {
    
    // Send the current number
    Serial.println(data1);
    delay(50);
    Serial.println(data2);
    delay(50);

}
