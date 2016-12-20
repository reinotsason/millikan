int level;
int adc_level;
char flag;

void setup()
{
	Serial.begin(115200);
	Serial.setTimeout(50); // Sets timeout for parseFloat to 50 ms

	analogWriteResolution(12);
	analogReadResolution(12);
  pinMode(A1, INPUT);

	level = 0x000; // Default to 0 output voltage
	analogWrite(DAC0, level);
}

void loop()
{
	if(Serial.available() > 0) {
		flag = Serial.read();
		if (flag == 'v') {
  			level = int(Serial.parseFloat());
  			analogWrite(DAC0, level);
		} else if (flag == 'r') {
			for (int i = 0; i < 64; i++) {
				adc_level += analogRead(A1);
				delay(1);
			}
			adc_level = adc_level / 64;
			Serial.println(adc_level);
		}
  	}
  	
  	delay(1);
}
