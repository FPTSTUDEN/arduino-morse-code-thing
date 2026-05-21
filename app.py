from flask import Flask, render_template, Response
from flask_cors import CORS
import serial
import time
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
MORSE_CODE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}
SERIAL_PORT = "COM8"
BAUD_RATE = 9600
ser = None


def init_serial():
    global ser
    # The Werkzeug reloader trick: This prevents Flask from opening
    # the serial port twice when debug=True is active.
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        try:
            print(f"Connecting to Arduino on {SERIAL_PORT}...")
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
            time.sleep(2)  # Wait for Arduino bootloader reset
            print("Serial connection established successfully!")
        except serial.SerialException as e:
            print(f"\n--- SERIAL ERROR ---")
            print(f"Could not open {SERIAL_PORT}: {e}")
            print("CRITICAL: Make sure the Arduino IDE Serial Monitor is CLOSED!\n")


def serial_stream():
    test_mode = False
    morse_text = ""
    global ser
    # Safety check if the port failed to open during startup
    if ser is None or not ser.is_open:
        print("data:  Error: Serial port not available \n\n")
        print("Reading mock data from file...")
        test_mode = True
        with open("sample.txt", "r") as f:
            for line in f:
                for char in line.strip():
                    morse_text += char
                    if char == " ":
                        letter = MORSE_CODE.get(morse_text.strip(), "")
                        if letter:
                            print(f"Received Morse: {morse_text.strip()} -> Letter: {letter}")
                        else:
                            print(f"Received Morse: {morse_text.strip()} -> Unknown")
                        morse_text = ""
                    yield f"data: {char}\n\n"
                    time.sleep(0.5)
        yield "data:  \n\n"  # Final space to trigger last letter translation
    
    while test_mode == False:
        try:
            if ser.in_waiting:
                # Read ALL available bytes currently waiting in the buffer
                # (This captures the whole ".  (450 ms)\n" string at once)
                morse = ser.read(ser.in_waiting).decode(errors="ignore")
                morse_text += morse
                if morse == " ":
                    letter = MORSE_CODE.get(morse_text.strip(), "")
                    if letter:
                        print(f"Received Morse: {morse_text.strip()} -> Letter: {letter}")
                    else:
                        print(f"Received Morse: {morse_text.strip()} -> Unknown")
                    morse_text = ""
                if morse:
                    yield f"data: {morse}\n\n"
        except (serial.SerialException, OSError) as e:
            print(f"Serial connection lost: {e}")
            yield "data: Connection lost\n\n"
            break

        # A tiny sleep prevents this loop from locking up 100% of your CPU
        time.sleep(0.05)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    return Response(
        serial_stream(),
        mimetype="text/event-stream"
    )


if __name__ == "__main__":
    # Initialize the serial port cleanly right before Flask fires up
    init_serial()
    app.run(debug=True)