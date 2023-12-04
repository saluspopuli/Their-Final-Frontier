# 1 "C:\\Users\\Andre\\Documents\\Coding Main\\Numerical Methods Project\\Arduino_Control\\Arduino_Control.ino"







int debounceDelay = 50; // Debounce delay in milliseconds
bool ledState = false;

int debounce(int pin)
{
    int currentState = digitalRead(pin);
    int lastState = currentState;
    unsigned long lastDebounceTime = 0;

    if (currentState != lastState) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
        currentState = digitalRead(pin);
        if (currentState != lastState) {
            lastState = currentState;
            return currentState;
        }
    }

    return lastState;
}

void setup()
{
    pinMode(4, 0x0);
    pinMode(3, 0x0);
    pinMode(A0, 0x0);
    pinMode(A1, 0x0);

    pinMode(2, 0x1);

 Serial.begin(115200);
}

void loop()
{
    if (Serial.available() > 0) {
        char data = Serial.read();

        if (data == '0') {
            ledState = true;
            Serial.println("Success!!!");
        } else if (data == '1'){
            ledState = false;
        }
    }

    if (ledState){
        digitalWrite(2, 0x1);
    } else {
        digitalWrite(2, 0x0);
    }

    Serial.print(analogRead(A1) - analogRead(A0));
    Serial.print(" ");
    Serial.print(debounce(4));
    Serial.print(" ");
    Serial.print(debounce(3));
    Serial.println();
}
