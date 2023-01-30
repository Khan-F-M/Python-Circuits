//Name: Khan, Muhammad
//Date: 3/13/2021

#include <wiringPi.h>
#include <signal.h>

#define RED 23
#define REDT 24
#define REDTH 25

int blink = 0;

void cleanup(int signo) {
     blink = 0;
}

int main(void) {
     signal(SIGINT, cleanup);
     signal(SIGTERM, cleanup);
     signal(SIGHUP, cleanup);

    wiringPiSetup();
    pinMode(RED, OUTPUT);
    pinMode(REDT, OUTPUT);
    pinMode(REDTH, OUTPUT);

    while(blink) {
        digitalWrite(RED, HIGH);
        delay(500);
        digitalWrite(RED, LOW);
        digitalWrite(REDT, HIGH);
        delay(500);
        digitalWrite(REDT, LOW);
        digitalWrite(REDTH, HIGH);
        delay(500);
        digitalWrite(REDTH, LOW);
      }

      digitalWrite(RED, LOW);
      digitalWrite(REDT, LOW);
      digitalWrite(REDTH, LOW);

      pinMode(RED, INPUT);
      pinMode(REDT, INPUT);
      pinMode(REDTH, INPUT);
      return 0;
}
