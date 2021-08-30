#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>


typedef struct {        // Struct is defined before including config.h --
  int8_t  select;       // pin numbers for each eye's screen select line
  uint8_t rotation;     // also display rotation.
} eyeInfo_t;

#include "config.h"     // ****** CONFIGURATION IS DONE IN HERE ******

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RESET);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print(F("Hello! Eye Test!"));
  //init to the size of your display
  //tft.init(TFT_HEIGHT,TFT_WIDTH);
  tft.initR(INITR_144GREENTAB); //init for adafruit 1.44 breakout
  tft.fillScreen(ST77XX_BLACK);
  tft.setRotation(eyeInfo[0].rotation);
    
}

SPISettings settings(SPI_FREQ, MSBFIRST, SPI_MODE0);

void loop() {
  // put your main code here, to run repeatedly:
  drawEye(1, 200, 20, 20, 5, 2);
  
}

void drawEye( // Renders one eye.  Inputs must be pre-clipped & valid.
  uint8_t  e,       // Eye array index; 0 or 1 for left/right
  uint32_t iScale,  // Scale factor for iris
  uint8_t  scleraX, // First pixel X offset into sclera image
  uint8_t  scleraY, // First pixel Y offset into sclera image
  uint8_t  uT,      // Upper eyelid threshold value
  uint8_t  lT) {    // Lower eyelid threshold value
  
    uint8_t  screenX, screenY, scleraXsave;
    int16_t  irisX, irisY;
    uint16_t p, a;
    uint32_t d;
    SPI.beginTransaction(settings);
    digitalWrite(eyeInfo[0].select,LOW);
    tft.setAddrWindow(0,0,128,128);
    digitalWrite(eyeInfo[0].select,LOW);
    digitalWrite(TFT_DC, HIGH);
    if (true) { //always draw
      scleraXsave = scleraX; // Save initial X value to reset on each line
      irisY       = scleraY - (SCLERA_HEIGHT - IRIS_HEIGHT) / 2;
      for(screenY=0; screenY<SCREEN_HEIGHT; screenY++, scleraY++, irisY++) {
      scleraX = scleraXsave;
      irisX   = scleraXsave - (SCLERA_WIDTH - IRIS_WIDTH) / 2;
      for(screenX=0; screenX<SCREEN_WIDTH; screenX++, scleraX++, irisX++) {
        if((lower[screenY][screenX] <= lT) ||
           (upper[screenY][screenX] <= uT)) {             // Covered by eyelid
          p = 0;
        } else if((irisY < 0) || (irisY >= IRIS_HEIGHT) ||
                  (irisX < 0) || (irisX >= IRIS_WIDTH)) { // In sclera
          p = sclera[scleraY][scleraX];
        } else {                                          // Maybe iris...
          p = polar[irisY][irisX];                        // Polar angle/dist
          d = (iScale * (p & 0x7F)) / 128;                // Distance (Y)
          if(d < IRIS_MAP_HEIGHT) {                       // Within iris area
            a = (IRIS_MAP_WIDTH * (p >> 7)) / 512;        // Angle (X)
            p = iris[d][a];                               // Pixel = iris
          } else {                                        // Not in iris
            p = sclera[scleraY][scleraX];                 // Pixel = sclera
          }
        }
      //need to do something with FIFO SPI to wait for things to be complete...
      delay(10);
     } // end column
    }
   }
}
