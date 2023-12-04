#define B1 4
#define B2 3
#define LED 2

#define LEFT A0
#define RIGHT A1

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
    pinMode(B1, INPUT);
    pinMode(B2, INPUT);
    pinMode(LEFT, INPUT);
    pinMode(RIGHT, INPUT);

    pinMode(LED, OUTPUT);
    
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
        digitalWrite(LED, HIGH);
    } else {
        digitalWrite(LED, LOW);
    }

    Serial.print(analogRead(RIGHT) - analogRead(LEFT));
    Serial.print(" ");
    Serial.print(debounce(B1));
    Serial.print(" ");
    Serial.print(debounce(B2));
    Serial.println();
}