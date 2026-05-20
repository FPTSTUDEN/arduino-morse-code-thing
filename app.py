from flask import Flask, render_template, Response
import serial
import time

app = Flask(__name__)

# Change COM port to yours
SERIAL_PORT = "COM3"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino reset


def serial_stream():
    while True:
        if ser.in_waiting:
            morse = ser.read().decode(errors="ignore")

            yield f"data: {morse}\n\n"


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
    app.run(debug=True)