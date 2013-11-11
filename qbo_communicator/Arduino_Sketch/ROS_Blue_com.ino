//bluetooth spark fun blusmirf Tx2 Rx3
#include <SoftwareSerial.h>

int bluetoothTx = 2;
int bluetoothRx = 3;

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup()
{
  //Setup usb serial connection to computer
  Serial.begin(115200);
Serial.println("115200");
  //Setup Bluetooth serial connection to android
  bluetooth.begin(115200);
  delay(100);
  bluetooth.println("U,115200,N");
  bluetooth.begin(115200);
}//bluetooth spark fun blusmirf Tx2 Rx3
#include <SoftwareSerial.h>

int bluetoothTx = 2;
int bluetoothRx = 3;

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup()
{
  //Setup usb serial connection to computer
  Serial.begin(115200);
Serial.println("115200");
  //Setup Bluetooth serial connection to android
  bluetooth.begin(115200);
  delay(100);
  bluetooth.println("U,115200,N");
  bluetooth.begin(115200);
}

void loop()
{
  //Read from bluetooth and write to usb serial
  if(bluetooth.available())
  {
    char toSend = (char)bluetooth.read();
    Serial.println(toSend);
  }

  //Read from usb serial to bluetooth
  if(Serial.available())
  {
    char toSend = (char)Serial.read();
    bluetooth.print(toSend);
    
  }
}

void loop()
{
  //Read from bluetooth and write to usb serial
  if(bluetooth.available())
  {
    char toSend = (char)bluetooth.read();
    Serial.print(toSend);
  }

  //Read from usb serial to bluetooth
  if(Serial.available())
  {
    char toSend = (char)Serial.read();
    bluetooth.print(toSend);
    
  }
}
