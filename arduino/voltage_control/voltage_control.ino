int level;
int adc_level;

void setup()
{
	Serial.begin(115200);
	Serial.setTimeout(50); // Sets timeout for parseFloat to 50 ms

	analogWriteResolution(12);
	analogReadResolution(12);

	level = 0x000; // Default to 0 output voltage
	analogWrite(DAC0, level);
}

void loop()
{
	if(Serial.available() > 0) {
  		level = int(Serial.parseFloat());
  		analogWrite(DAC0, level);
  	}
  	
  	adc_level = analogRead(A7);
  	delay(2);
}
