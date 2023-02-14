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

void setup() {
  Serial.begin(9600);
  Serial.println("Serial 1 Connected");

  pinPeripheral(SDA, PIO_SERCOM);
  pinPeripheral(SCL, PIO_SERCOM);

  //setting up serial 2
  Serial2.begin(9600);
  Serial.println("Serial 2 Connected");
}

void loop(){
  Serial.println("Talking");
  //if GPS there, show data, is Serial2 doesn't work, show error
  if(Serial2.available()){
    showData();
  }
  else{
    Serial.println("Serial2 not available");
  }
  //delay(1000);
}
