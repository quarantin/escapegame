#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>

PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);

int DownstopButton = 4;
int UpstopButton = 5;
int in1pin = 6;
int in2pin = 7; // h bridge pins
int Raspi = 13;
int RaspiSignal = 12;
int successState = 0;
boolean up = true;
uint8_t good[4] = {118, 221, 89, 31};
bool statut = 1;
bool has_lift = 1;

void read_good_tag_id_from_serial(uint8_t *uid, size_t uidsz)
{
  char sbuf[3];
  char tag_id[uidsz * 2 + 1];

  // We need at least uidsz * 2 because we are reading hexadecimal characters
  if (Serial.available() < uidsz * 2)
    return;

  // Read tag ID as hexadecimal from serial (uidsz * 2 characters)
  for (int i = 0; i < uidsz * 2; i++)
    tag_id[i] = (char)Serial.read();

  // For each pair of hexadecimal character (== one byte)
  for (int i = 0, j = 0; i < uidsz * 2; i+=2, j++) {

    // Copy the pair of hexadecimal characters to sbuf and make a string out of it
    sbuf[0] = tag_id[i + 0];
    sbuf[1] = tag_id[i + 1];
    sbuf[2] = 0;

    // Convert the resulting hexadecimal string into a byte
    uid[j] = (uint8_t)strtoul(sbuf, NULL, 16);
  }

  // Just for debug
  // Write null byte at the end of tag_id so we can use it as a string
  //tag_id[uidsz * 2] = 0;
  //Serial.print("New cube ID: ");
  //Serial.print(tag_id);
  //Serial.println();
}

void setup() {
  pinMode(in1pin, OUTPUT);
  pinMode(in2pin, OUTPUT); // outputs
  pinMode(Raspi, OUTPUT);
  pinMode(RaspiSignal, INPUT);
  pinMode(DownstopButton, INPUT_PULLUP);
  pinMode(UpstopButton, INPUT_PULLUP);
  Serial.begin(9600);

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }

  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata >> 24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata >> 16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata >> 8) & 0xFF, DEC);

  // Set the max number of retry attempts to read from a card
  // This prevents us from waiting forever for a card, which is
  // the default behaviour of the PN532.
  nfc.setPassiveActivationRetries(0xFF);

  // configure board to read RFID tags
  nfc.SAMConfig();

  Serial.println("Waiting for an ISO14443A card");

}

void loop() {

  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

  int UpstopButtonState = digitalRead(UpstopButton);
  int DownstopButtonState = digitalRead(DownstopButton);
  int RaspiSignalState = digitalRead(RaspiSignal);

  int cube_present = LOW;

  read_good_tag_id_from_serial(good, sizeof(good));

  Serial.println(RaspiSignalState);
  if (success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength)) {
    if (uid[0] == good[0]   // Si l'UID 0  est égale à 1
        && uid[1] == good[1]   // Et si l'UID 1  est égale à 171
        && uid[2] == good[2]   // Et si l'UID 2  est égale à 43
        && uid[3] == good[3])  // Et si l'UID 4  est égale à 224
    {
      cube_present = HIGH;
    }
  }

  //digitalWrite(Raspi, HIGH);
  Serial.println(RaspiSignalState);
  //Serial.println(DownstopButtonState);
  //Serial.println(UpstopButtonState);
  //Serial.println(RaspiSignalState);

  if (cube_present == LOW)
    Serial.println("bad");
  else
    Serial.println("good");

  digitalWrite(Raspi, cube_present);

  if (has_lift) {

    if (RaspiSignalState == HIGH) {

      if (!DownstopButtonState) {

        digitalWrite(in1pin, HIGH); // make motor go one way
        delay(1);
        digitalWrite(in2pin, LOW);
      }

      if (!UpstopButtonState) {

        digitalWrite(in1pin, LOW); // make motor stop at top
        delay(1);
        digitalWrite(in2pin, LOW);
        delay(5000);
      }
    }

    else if (RaspiSignalState == LOW) {

      if (!DownstopButtonState) {

        digitalWrite(in1pin, LOW); //  make motor go the other way
        delay(1);
        digitalWrite(in2pin, LOW);
      }

      if (!UpstopButtonState) {

        digitalWrite(in1pin, LOW); //  make motor go the other way
        delay(1);
        digitalWrite(in2pin, HIGH);
      }
    }
  }
  delay(50);
}
