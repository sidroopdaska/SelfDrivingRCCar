// Pin Numbers
int forward_pin = 6;
int reverse_pin = 7;
int left_pin = 8;
int right_pin = 9;

// Initial command
int command = 0;

// PPWM Durations (in ms)
int on_time = 30;
int off_time = 70;

void setup() {
  // Set pins to OUTPUT mode
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(right_pin, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    command = Serial.read();
  }
  else
  {
    reset();
  }

   drive(command);
}

void reset()
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, HIGH);
}

// alternatively try 40/60, 250/500
void forward(int complex)
{
  if(complex == 0)
  {
    digitalWrite(reverse_pin, HIGH);
    digitalWrite(left_pin, HIGH);
    digitalWrite(right_pin, HIGH);
  } 
  
  digitalWrite(forward_pin, LOW);
  delay(50);
  digitalWrite(forward_pin, HIGH);
  delay(50);
}

// alternatively try: 50/50
void reverse(int complex)
{
  if(complex == 0)
  {
    digitalWrite(forward_pin, HIGH);
    digitalWrite(left_pin, HIGH);
    digitalWrite(right_pin, HIGH);
  } 
  
  digitalWrite(reverse_pin, LOW);
  delay(55);
  digitalWrite(reverse_pin, HIGH);
  delay(45);
}

void left()
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  delay(on_time);
}

void right()
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  delay(on_time);
}

void forward_right()
{
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  forward(1);
}


void forward_left()
{
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  forward(1);
}

void reverse_right()
{
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  reverse(1);
}

void reverse_left()
{
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  reverse(1);
}

void drive(int command)
{
  switch(command)
  {
    case 48: reset(); break;
    case 49: forward(0); break;
    case 50: reverse(0); break;
    case 51: right(); break;
    case 52: left(); break;
    case 53: forward_right(); break;
    case 54: forward_left(); break;
    case 55: reverse_right(); break;
    case 56: reverse_left(); break;
    default: break;
  }
}
