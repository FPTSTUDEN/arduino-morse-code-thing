from flask import Flask, render_template, Response, jsonify
import serial
import threading
import time

app = Flask(__name__)

# -----------------------------
# Config
# -----------------------------
import os

SERIAL_PORT = os.environ.get("SERIAL_PORT", "COM7")
BAUD_RATE = 9600

# -----------------------------
# Morse translation
# -----------------------------
MORSE_DICT = {
    ".-": "A", "-...": "B",
    "-.-.": "C", "-..": "D",
    ".": "E", "..-.": "F",
    "--.": "G", "....": "H",
    "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N",
    "---": "O", ".--.": "P",
    "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T",
    "..-": "U", "...-": "V",
    ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}

# -----------------------------
# Shared state
# -----------------------------
raw_morse = ""
translated_message = ""
current_letter = ""

lock = threading.Lock()

# -----------------------------
# Serial setup
# -----------------------------
ser = None  # Will be initialized in main

# -----------------------------
# Background serial reader
# -----------------------------
def serial_worker():
    global raw_morse
    global translated_message
    global current_letter
    while True:
        try:
            if ser and ser.in_waiting:
                char = ser.read().decode(
                    errors="ignore"
                )

                with lock:
                    raw_morse += char

                    # Space means end of letter
                    if char == " ":

                        if current_letter:
                            translated_message += (
                                MORSE_DICT.get(
                                    current_letter,
                                    "?"
                                )
                            )

                            current_letter = ""

                    else:
                        current_letter += char

        except serial.SerialException as e:
            print(f"Serial exception: {e}")
            try:
                ser.close()
            except Exception:
                pass
            time.sleep(2)
            try:
                ser = serial.Serial(
                    SERIAL_PORT,
                    BAUD_RATE,
                    timeout=1
                )
                print("Reconnected to serial port.")
            except Exception as reconnect_error:
                print(f"Reconnection failed: {reconnect_error}")
                ser = None
                time.sleep(5)
        except Exception as e:
            print(f"Unexpected error in serial_worker: {e}")
            time.sleep(1)

        time.sleep(0.01)

        time.sleep(0.01)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template(
        "index.html"
    )


@app.route("/stream")
def stream():

    def event_stream():
        last_seen = 0

        while True:
            with lock:
                current = raw_morse

            if len(current) > last_seen:
                new_data = current[last_seen:]

                yield (
                    f"data: "
                    f"{new_data}\n\n"
                )

                last_seen = len(current)

            time.sleep(0.05)

    return Response(
        event_stream(),
        mimetype=
        "text/event-stream"
    )
@app.route("/translated")
def translated():
    """
    Returns:
        JSON object with the following format:
        {
            "message": "<translated_message>"
        }
        - message: The translated text from Morse code as a string.
    """
    with lock:
    # Delay after opening serial port to allow hardware reset (common for Arduino boards)
    SERIAL_INIT_DELAY = 2  # seconds; make configurable if needed

    try:
        ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=1
        )
        time.sleep(SERIAL_INIT_DELAY)  # Wait for hardware to initialize
        threading.Thread(
            target=serial_worker,
            daemon=True
        ).start()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None
            timeout=1
        )
        time.sleep(2)
    # WARNING: Do not use debug=True in production!
    app.run(debug=True)d(
            target=serial_worker,
            daemon=True
        ).start()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None

    app.run(debug=True)