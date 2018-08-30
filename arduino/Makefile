ARDUINO    := ~/golang/bin/arduino-cli

BOARD_UNO  := arduino:avr:uno
PORT_UNO   := /dev/ttyUSB0

BOARD_MEGA := arduino:avr:mega:cpu=atmega2560
PORT_MEGA  := /dev/ttyACM0

SKETCH     := nfc/

arduino/uno: uno_compile uno_install

arduino/mega: mega_compile mega_install

uno_compile:
	$(ARDUINO) compile -b $(BOARD_UNO) $(SKETCH)

mega_compile:
	$(ARDUINO) compile -b $(BOARD_MEGA) $(SKETCH)

uno_install:
	$(ARDUINO) upload -b $(BOARD_UNO) -p $(PORT_UNO) $(SKETCH)

mega_install:
	$(ARDUINO) upload -b $(BOARD_MEGA) -p $(PORT_MEGA) $(SKETCH)

.PHONY: arduino/uno arduino/mega
