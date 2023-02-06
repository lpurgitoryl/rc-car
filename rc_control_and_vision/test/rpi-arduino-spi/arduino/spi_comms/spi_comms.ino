#include <SPI.h>
char buff [50];
volatile byte indx;
volatile boolean process;
// MOSI - pin 11
// MISO - pin 12
// SCLK - pin 13

void setup (void) {
   Serial.begin (115200);
   pinMode(MISO, OUTPUT); // have to send on master in so it set as output
   SPCR |= _BV(SPE); // turn on SPI in slave mode
   indx = 0; // buffer empty
   process = false;
  //  SPI.attachInterrupt(); // turn on interrupt
}

byte handler(){
  byte in_byte;
  // SPIF indicates transmission complete (byte received)
  if ((SPSR & (1 << SPIF)) != 0)
  {
    in_byte = SPDR;
    Serial.println("recv'd this");
    Serial.println(in_byte);
    // Handle the input code here
    // Set return_val to the value you want to return  
  }
  return 'c'
}

void loop (void) {
  //  if (process) {
  //     process = false; //reset the process
  //     Serial.println (buff); //print the array on serial monitor
  //     indx= 0; //reset button to zero
  //  }
  SPDR = handler();

}