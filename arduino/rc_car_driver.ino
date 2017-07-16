// Pin Numbers
int forward_pin = 6;
int reverse_pin = 7;
int left_pin = 8;
int right_pin = 9;

// Initial command
int command = 0;

// Duration for output (in ms)
int time = 50;

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

  drive(command, time);
}

void reset()
{
  digitalWrite(forward_pin, HIGH); 
  digitalWrite(reverse_pin, HIGH); 
  digitalWrite(left_pin, HIGH); 
  digitalWrite(right_pin, HIGH); 
}

void forward(int time)
{
  digitalWrite(forward_pin, LOW);
  delay(time);
}


void reverse(int time)
{
  digitalWrite(reverse_pin, LOW);
  delay(time);
}


void left(int time)
{
  digitalWrite(left_pin, LOW);
  delay(time);
}


void right(int time)
{
  digitalWrite(right_pin, LOW);
  delay(time);
}

void forward_right(int time)
{
  digitalWrite(forward_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void forward_left(int time)
{
  digitalWrite(forward_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);
}

void reverse_right(int time)
{
  digitalWrite(reverse_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void reverse_left(int time)
{
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);
}

void drive(int command, int time)
{
  switch(command)
  {
    case 0: reset(); break;
    case 1: forward(time); break;
    case 2: reverse(time); break;
    case 3: right(time); break;
    case 4: left(time); break;

    case 5: forward_right(time); break;
    case 6: forward_left(time); break;
    case 7: reverse_right(time); break;
    case 8: reverse_left(time); break;

    default: Serial.print("Invalud command! \n");
  }
}

