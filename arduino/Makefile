BOARD=arduino:sam:due
PORT=/dev/ttyACM0
INO_FILE=voltage_control.ino

upload: $(FILE)
	arduino --upload --board $(BOARD) --port $(PORT) -v $(INO_FILE)

verify: $(FILE)
	arduino --verify --board $(BOARD) --port $(PORT) -v $(INO_FILE)
