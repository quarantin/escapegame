#include <Wire.h>
#include "PN532_I2C.h"
#include <PN532.h>
#include <NfcAdapter.h>

#define BLINK_DELAY 100
#define SERIAL_BAUDS 9600
#define MSG_TAG_ENTER "TAG-ENTER-"
#define MSG_TAG_LEAVE "TAG-LEAVE"

#define PIN_TABLE 12

#define debug() Serial.println(__func__)

int cube_present;
int saved_cube_present;

char *last_command, tag[5];

PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);

/**
 * Blink the Arduino LED n times.
 */
void blink(int n)
{
	while (n--) {

		digitalWrite(LED_BUILTIN, HIGH);
		delay(BLINK_DELAY);

		digitalWrite(LED_BUILTIN, LOW);
		delay(BLINK_DELAY);
	}

	delay(BLINK_DELAY * 5);
}

/**
 * Halt the Arduino (infinite loop, with LED blinking).
 */
void halt()
{
	while (1)
		blink(1);
}

/**
 * Reset the state of the Arduino.
 */
void arduino_reset()
{
	debug();
	blink(10);

	cube_present = 0;

	saved_cube_present = 0;

	last_command = NULL;

	memset(tag, 0, sizeof(tag));
}

/**
 * Raise the cube.
 */
void raise_cube()
{
	debug();
	blink(10);

	digitalWrite(PIN_TABLE, HIGH);
}

/**
 * Lower the cube.
 */
void lower_cube()
{
	debug();
	blink(10);

	digitalWrite(PIN_TABLE, LOW);
}

/**
 * Check the version of our PN532 chip.
 */
void check_version()
{
	uint32_t version= nfc.getFirmwareVersion();
	if (!version) {
		Serial.println("Could not find PN532 board");
		halt();
	}

	Serial.print("Found chip PN5");
	Serial.println((version >> 24) & 0xff, HEX);

	Serial.print("Firmware ver.");
	Serial.println((version >> 16) & 0xff, DEC);

	Serial.print(".");
	Serial.println((version >>  8) & 0xff, DEC);
}

/**
 * Read NFC tag and copy tag ID in buf.
 */
int read_nfc_tag(char *buf, size_t bufsz)
{
	int success;

	blink(3);

	success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, buf, bufsz);

	return !success;
}

/**
 * Read a line of text from serial.
 */
int readline(char *buf, size_t bufsz)
{
	int i;
	char c;

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
	pinMode(PIN_TABLE, OUTPUT);

	arduino_reset();

	nfc.begin();

	check_version();

	nfc.setPassiveActivationRetries(0xff);

	nfc.SAMConfig();
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
