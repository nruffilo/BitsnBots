/*
  Analog Plotting Test
  
  This file is meant to show the outputs of an analog or digital sensor
  
  Use this with the Arduino Plotting tool to see the output visually
*/

int sensorPin = A0;    // select the input pin you are using

void setup() {
	Serial.begin(9600); // initialize the serial connection
}

void loop() {
	Serial.println(analogRead(sensorPin)); //Output the sensor value
	delay(100); //delay 100 ms - you can make this shorter or longer for more detailed
				//readings, but values too low may not get consistent readings.
}
