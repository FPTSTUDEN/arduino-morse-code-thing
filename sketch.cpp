#include <LiquidCrystal.h>

int seconds = 0;
int buttonPin = 7;
int buttonState;
int holdTime = 0;

LiquidCrystal lcd_1(12, 11, 5, 4, 3, 2);

void setup()
{
  lcd_1.begin(16, 2);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop()
{
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    lcd_1.clear();
  }
  else {
    holdTime += 1;
    if (holdTime < 3) {;
      lcd_1.print(".");
    }
    else {
      lcd_1.print("_");
    }
  }
  delay(200);
}