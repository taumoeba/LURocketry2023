#include <Arduino.h>   // required before wiring_private.h
#include <TinyGPS++.h>
#include "wiring_private.h" // pinPeripheral() function
#include <SPI.h>
#include <RH_RF95.h>
#include <string.h>

#define RFM95_CS 10
#define RFM95_RST 11
#define RFM95_INT 6

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

Uart Serial2 (&sercom3, SDA, SCL, SERCOM_RX_PAD_1, UART_TX_PAD_0);
                     // TX   RX
void SERCOM3_Handler()
{
  Serial2.IrqHandler();
}

TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);

  Serial2.begin(9600);
  
  // Assign pins 10 & 11 SERCOM functionality
  pinPeripheral(SDA, PIO_SERCOM);
  pinPeripheral(SCL, PIO_SERCOM);

  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

int16_t packetnum = 0;  // packet counter, we increment per xmission
char in[2] = {'0','0'};

uint8_t i=0;
void loop() {
  
  /* // ONLY READING FROM SERIAL
  while (Serial2.available() > 0){
    //Serial.println("available");
    Serial.write(Serial2.read());
  }
  */

  /* // READING FROM GPS AND PRINTING TO SERIAL
  while (Serial2.available() > 0)
    if (gps.encode(Serial2.read()))
      showData();
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println("GPS NOT DETECTED!");
    //while(true);
  }
  */

  // READING FROM GPS AND TRANSMITTING OVER RADIO
  while (Serial2.available() > 0)
    if (gps.encode(Serial2.read()))
      sendData();
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println("GPS NOT DETECTED!");
    //while(true);
  }
  
 // delay(1000);
}

void showData()
{
  if (gps.location.isValid())
  {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
    Serial.print("Altitude: ");
    Serial.println(gps.altitude.meters());
  }
  else
  {
    Serial.println("Location is not available");
  }
  
  Serial.print("Date: ");
  if (gps.date.isValid())
  {
    Serial.print(gps.date.month());
    Serial.print("/");
    Serial.print(gps.date.day());
    Serial.print("/");
    Serial.println(gps.date.year());
  }
  else
  {
    Serial.println("Not Available");
  }

  Serial.print("Time: ");
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    Serial.print(gps.time.hour());
    Serial.print(":");
    if (gps.time.minute() < 10) Serial.print(F("0"));
    Serial.print(gps.time.minute());
    Serial.print(":");
    if (gps.time.second() < 10) Serial.print(F("0"));
    Serial.print(gps.time.second());
    Serial.print(".");
    if (gps.time.centisecond() < 10) Serial.print(F("0"));
    Serial.println(gps.time.centisecond());
  }
  else
  {
    Serial.println("Not Available");
  }

  Serial.println();
  Serial.println();
  //delay(5000);
}

void sendData()
{
  if (gps.location.isValid())
  {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    double lati = gps.location.lat();
    double longi = gps.location.lng();
    Serial.println(lati,6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
    Serial.println(longi,6);
    char longBuf[10];
    char latBuf[9];
    char * cp = latBuf;
    char * cp2 = longBuf;
    unsigned long l, l2, rem, rem2;
    if(lati<0) {
      *cp++ = '-';
      lati = -lati;
    }
    if(longi<0) {
      *cp2++ = '-';
      longi = -longi;
    }
    l = (unsigned long)lati;
    l2 = (unsigned long)longi;
    lati -= (double)l;
    longi -= (double)l2;
    rem = (unsigned long)(lati*1e6);
    rem2 = (unsigned long)(longi*1e6);
    sprintf(cp,"%lu.%6.6lu", l, rem);
    sprintf(cp2, "%lu.%6.6lu", l2, rem2);
    
    for(int i=0; i<9; i++) Serial.print(latBuf[i]);
    Serial.println();
    for(int i=0; i<10; i++) Serial.print(longBuf[i]);
    Serial.println();
    rf95.send((uint8_t *)latBuf, 9);
    rf95.send((uint8_t *)longBuf, 10);
  }
  else
  {
    Serial.println("Location is not available");
  }
}