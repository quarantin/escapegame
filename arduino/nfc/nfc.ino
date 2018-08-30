#define BLINK_DELAY 100
#define SERIAL_BAUDS 9600
#define MSG_TAG_ENTER "TAG-ENTER-"
#define MSG_TAG_LEAVE "TAG-LEAVE"

#define debug() Serial.println(__func__)

int cube_present;
int saved_cube_present;

char *last_command, tag[5];

/**
 * Blink the Arduino LED n times.
 */
void blink(int n)
{
	debug();

	while (n--) {

		digitalWrite(LED_BUILTIN, HIGH);
		delay(BLINK_DELAY);

		digitalWrite(LED_BUILTIN, LOW);
		delay(BLINK_DELAY);
	}

	delay(BLINK_DELAY * 5);
}

/**
 * Reset the state of the Arduino.
 */
void arduino_reset()
{
	debug();

	cube_present = 0;

	saved_cube_present = 0;

	last_command = NULL;

	memset(tag, 0, sizeof(tag));

	blink(10);
}

/**
 * Raise the cube.
 */
void raise_cube()
{
	debug();

	// TODO
	// raise the cube table
	blink(2);
}

/**
 * Lower the cube.
 */
void lower_cube()
{
	debug();

	// TODO
	// lower the cube table
	blink(3);
}

/**
 * Read NFC tag and copy tag ID in buf.
 */
int read_nfc_tag(char *buf, size_t bufsz)
{
	debug();

	// TODO
	// get NFC tag with reader, timeout should be less than a second.
	blink(4);
	return -1;
}

/**
 * Read a line of text from serial.
 */
int readline(char *buf, size_t bufsz)
{
	int i;
	char c;

	debug();

	for (i = 0; i < bufsz; i++)
		buf[i] = 0;

	i = 0;
	while (Serial.available() && i < bufsz - 1) {

		c = Serial.read();
		if (c == '\n') {
			buf[i] = 0;
			break;
		}

		buf[i++] = c;
	}

	return i;
}

/**
 * Setup function.
 */
void setup()
{
	Serial.begin(SERIAL_BAUDS);

	while (!Serial) {
		; // wait for serial port to connect. Needed for native USB port only
	}

	Serial.println("Hello Serial!");

	pinMode(LED_BUILTIN, OUTPUT);

	arduino_reset();
}

/**
 * Loop function.
 */
void loop()
{
	int err, count;
	char command[32];

	// Check if the master sent us some commands
	count = readline(command, sizeof(command));
	if (count > 0) {

		// Reset the arduino state
		if (!strcmp(command, "reset"))
			arduino_reset();

		// Raise the cube
		else if (!strcmp(command, "raise-cube"))
			raise_cube();

		// Lower the cube
		else if (!strcmp(command, "lower-cube"))
			lower_cube();
	}

	// In all cases we want to notify the master of change events
	// (i.e. tag just left, or tag just arrived)

	saved_cube_present = cube_present;

	// Read a tag with the NFC reader
	err = read_nfc_tag(tag, sizeof(tag));
	cube_present = !err;

	// If the state has changed, then we want to notify the master about it
	if (cube_present != saved_cube_present) {

		if (!cube_present)
			Serial.println(MSG_TAG_LEAVE);

		else {
			Serial.print(MSG_TAG_ENTER);
			Serial.println(tag);
		}
	}
}
