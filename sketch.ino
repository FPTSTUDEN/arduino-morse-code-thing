#include <LiquidCrystal.h>

// LCD pins: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int buttonPin = 7;

const int minPress = 50;      // Ignore under 50ms
const int dashThreshold = 400;

bool lastButtonState = HIGH;
unsigned long pressStart = 0;

String morseText = "";

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);

  lcd.begin(16, 2);
  lcd.print("Morse Input");

  Serial.begin(9600);

  // Prevent startup glitch
  lastButtonState =
    digitalRead(buttonPin);
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

    char symbol;

    // Ignore tiny presses (<50ms)
    if (pressDuration < minPress) {
      lastButtonState =
        currentButtonState;
      return;
    }

    // Dot or dash
    if (pressDuration < dashThreshold) {
      symbol = '.';
    } else {
      symbol = '-';
    }

    morseText += symbol;

    // LCD
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

    // Serial monitor
    Serial.print(symbol);
    Serial.print("  (");
    Serial.print(pressDuration);
    Serial.println(" ms)");
  }

  lastButtonState =
    currentButtonState;
}