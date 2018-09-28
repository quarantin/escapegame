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
int good[4] = {118, 221, 89, 31};
bool statut = 1;

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

  Serial.println(RaspiSignalState);
  if (success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength)) {
    if (uid[0] == good[0]   // Si l'UID 0  est égale à 1
        && uid[1] == good[1]   // Et si l'UID 1  est égale à 171
        && uid[2] == good[2]   // Et si l'UID 2  est égale à 43
        && uid[3] == good[3])  // Et si l'UID 4  est égale à 224
    {
      //digitalWrite(Raspi, HIGH);
      Serial.println(RaspiSignalState);
      Serial.println("good");
      //Serial.println(DownstopButtonState);
      //Serial.println(UpstopButtonState);
      //Serial.println(RaspiSignalState);

      if (!DownstopButtonState && RaspiSignalState == HIGH) {
        digitalWrite(in1pin, HIGH); // make motor go one way
        delay(1);
        digitalWrite(in2pin, LOW);
      }
      if (!UpstopButtonState && RaspiSignalState == LOW) { // if left button is pressed ...
        digitalWrite(Raspi, HIGH);
        digitalWrite(in1pin, LOW); //  make motor go the other way
        delay(1);
        digitalWrite(in2pin, HIGH);
      }
      if (!UpstopButtonState && RaspiSignalState == HIGH) {
        digitalWrite(in1pin, LOW); // make motor stop at top
        delay(1);
        digitalWrite(in2pin, LOW);
        delay(5000);
      }
      if (!DownstopButtonState && RaspiSignalState == LOW) {
        digitalWrite(in1pin, LOW); //  make motor go the other way
        delay(1);
        digitalWrite(in2pin, LOW);
      }
    } else {
      Serial.println("bad");
    }
  }
  delay(50);
}
