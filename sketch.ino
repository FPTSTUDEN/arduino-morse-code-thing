#include <LiquidCrystal.h>

// LCD pins: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int buttonPin = 7;

const int minPress = 50;      // Ignore under 50ms
const int dashThreshold = 400;

// Pause detection
const unsigned long spaceDelay = 1500;

bool lastButtonState = HIGH;

unsigned long pressStart = 0;
unsigned long lastInputTime = 0;

bool spaceSent = false;

String morseText = "";

void setup() {
  // lcd.print("HELLO WORLD");
  pinMode(buttonPin, INPUT_PULLUP);

  lcd.begin(16, 2);
  lcd.print("Morse Input");

  Serial.begin(9600);

  // Prevent startup glitch
  lastButtonState =
    digitalRead(buttonPin);

  lastInputTime = millis();
}

void loop() {

  bool currentButtonState =
    digitalRead(buttonPin);

  // Button pressed
  if (lastButtonState == HIGH &&
      currentButtonState == LOW) {

    pressStart = millis();
  }

  // Button released
  if (lastButtonState == LOW &&
      currentButtonState == HIGH) {

    unsigned long pressDuration =
      millis() - pressStart;

    // Ignore bounce (<50ms)
    if (pressDuration >= minPress) {

      char symbol;

      // Dot or dash
      if (pressDuration < dashThreshold) {
        symbol = '.';
      } else {
        symbol = '-';
      }

      morseText += symbol;

      Serial.print(symbol);

      // Reset space timer
      lastInputTime = millis();
      spaceSent = false;

      // LCD update
      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("Morse:");

      lcd.setCursor(0, 1);

    // Show only last 16 chars
      if (morseText.length() > 16) {
        lcd.print(
          morseText.substring(
            morseText.length() - 16
          )
        );
      } else {
        lcd.print(morseText);
      }
    }
  }

  // Space detection
  if (!spaceSent &&
      millis() - lastInputTime >
      spaceDelay) {

    Serial.print(" ");

    morseText += " ";

    spaceSent = true;
  }

  lastButtonState =
    currentButtonState;
}