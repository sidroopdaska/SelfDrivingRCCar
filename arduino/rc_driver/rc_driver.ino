// Pin Numbers
int forward_pin = 6;
int reverse_pin = 7;
int left_pin = 8;
int right_pin = 9;

// Initial command
int command = 0;

// Duration for output (in ms)
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

   drive(command, on_time, off_time);
}

void reset()
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, HIGH);
}

void forward(int one_time, int off_time, int c)
{
  if(c == 0)
  {
    digitalWrite(reverse_pin, HIGH);
    digitalWrite(left_pin, HIGH);
    digitalWrite(right_pin, HIGH);
  } 
  
  digitalWrite(forward_pin, LOW);
  delay(on_time);
  digitalWrite(forward_pin, HIGH);
  delay(off_time);
//  digitalWrite(forward_pin, LOW);
//  digitalWrite(reverse_pin, HIGH);
//  digitalWrite(left_pin, HIGH);
//  digitalWrite(right_pin, HIGH);
//  delay(on_time);
//  reset();
//  delay(off_time);
}

void reverse(int on_time, int off_time)
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, HIGH);
  delay(on_time);
  reset();
  delay(off_time);
}

void left(int on_time, int off_time)
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  delay(on_time);
  reset();
  delay(off_time);

}

void right(int on_time, int off_time)
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  delay(on_time);
  reset();
  delay(off_time);
}

void forward_right(int on_time, int off_time)
{
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  delay(on_time);
  reset();
  delay(off_time);
}


void forward_left(int on_time, int off_time)
{
  digitalWrite(reverse_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  forward(on_time, off_time, 1);
}

void reverse_right(int on_time, int off_time)
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, HIGH);
  digitalWrite(right_pin, LOW);
  delay(on_time);
  reset();
  delay(off_time);
}

void reverse_left(int on_time, int off_time)
{
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(right_pin, HIGH);
  delay(on_time);
  reset();
  delay(off_time);
}

void drive(int command, int one_time, int off_time)
{
  switch(command)
  {
    case 48: reset(); break;
    case 49: forward(on_time, off_time, 0); break;
    case 50: reverse(on_time, off_time); break;
    case 51: right(on_time, off_time); break;
    case 52: left(on_time, off_time); break;
    case 53: forward_right(on_time, off_time); break;
    case 54: forward_left(on_time, off_time); break;
    case 55: reverse_right(on_time, off_time); break;
    case 56: reverse_left(on_time, off_time); break;
    default: break;
  }
}
