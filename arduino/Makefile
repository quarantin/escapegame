ARDUINO := arduino-cli

BOARD := arduino:avr:mega:cpu=atmega2560
SKETCH := nfc/

PORT := /dev/ttyACM0

all:
	$(ARDUINO) compile -b $(BOARD) $(SKETCH)

install:
	$(ARDUINO) upload -b $(BOARD) -p $(PORT) $(SKETCH)
