#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>


typedef struct {        // Struct is defined before including config.h --
  int8_t  select;       // pin numbers for each eye's screen select line
  uint8_t rotation;     // also display rotation.
} eyeInfo_t;

uint32_t startTime;  // For FPS indicator

#include "config.h"     // ****** CONFIGURATION IS DONE IN HERE ******

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RESET);

void setup() {
  // put your setup code here, to run once:graphicsgraphics
  Serial.begin(9600);
  Serial.print(F("Hello! Eye Test!"));
  //init to the size of your display
  //tft.init(TFT_HEIGHT,TFT_WIDTH);
  tft.initR(INITR_144GREENTAB); //init for adafruit 1.44 breakout
  tft.fillScreen(ST77XX_BLACK);
  tft.setRotation(eyeInfo[0].rotation);
  startTime = millis(); // For frame-rate calculation
}

SPISettings settings(SPI_FREQ, MSBFIRST, SPI_MODE0);


const uint8_t ease[] = { // Ease in/out curve for eye movements 3*t^2-2*t^3
    0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  2,  2,  2,  3,   // T
    3,  3,  4,  4,  4,  5,  5,  6,  6,  7,  7,  8,  9,  9, 10, 10,   // h
   11, 12, 12, 13, 14, 15, 15, 16, 17, 18, 18, 19, 20, 21, 22, 23,   // x
   24, 25, 26, 27, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39,   // 2
   40, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 56, 57, 58,   // A
   60, 61, 62, 63, 65, 66, 67, 69, 70, 72, 73, 74, 76, 77, 78, 80,   // l
   81, 83, 84, 85, 87, 88, 90, 91, 93, 94, 96, 97, 98,100,101,103,   // e
  104,106,107,109,110,112,113,115,116,118,119,121,122,124,125,127,   // c
  128,130,131,133,134,136,137,139,140,142,143,145,146,148,149,151,   // J
  152,154,155,157,158,159,161,162,164,165,167,168,170,171,172,174,   // a
  175,177,178,179,181,182,183,185,186,188,189,190,192,193,194,195,   // c
  197,198,199,201,202,203,204,205,207,208,209,210,211,213,214,215,   // o
  216,217,218,219,220,221,222,224,225,226,227,228,228,229,230,231,   // b
  232,233,234,235,236,237,237,238,239,240,240,241,242,243,243,244,   // s
  245,245,246,246,247,248,248,249,249,250,250,251,251,251,252,252,   // o
  252,253,253,253,254,254,254,254,254,255,255,255,255,255,255,255 }; // n

void loop() {
  frame(200);
  /*
  // put your main code here, to run repeatedly:
  drawEye(0, 200, 20, 20, 5, 100);
  delay(100);
  Serial.println("Drawing eye...");
  */  
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


void frame( // Process motion for a single frame of left or right eye
  uint16_t        iScale) {     // Iris scale (0-1023) passed in
  static uint32_t frames   = 0; // Used in frame rate calculation
  static uint8_t  eyeIndex = 0; // eye[] array counter
  int16_t         eyeX, eyeY;
  uint32_t        t = micros(); // Time at start of function

  if(!(++frames & 255)) { // Every 256 frames...
    uint32_t elapsed = (millis() - startTime) / 1000;
    if(elapsed) Serial.println(frames / elapsed); // Print FPS
  }

  eyeIndex = 0; // Cycle through eyes, 1 per call

  // X/Y movement

  static boolean  eyeInMotion      = false;
  static int16_t  eyeOldX=512, eyeOldY=512, eyeNewX=512, eyeNewY=512;
  static uint32_t eyeMoveStartTime = 0L;
  static int32_t  eyeMoveDuration  = 0L;

  int32_t dt = t - eyeMoveStartTime;      // uS elapsed since last eye event
  if(eyeInMotion) {                       // Currently moving?
    if(dt >= eyeMoveDuration) {           // Time up?  Destination reached.
      eyeInMotion      = false;           // Stop moving
      eyeMoveDuration  = random(3000000); // 0-3 sec stop
      eyeMoveStartTime = t;               // Save initial time of stop
      eyeX = eyeOldX = eyeNewX;           // Save position
      eyeY = eyeOldY = eyeNewY;
    } else { // Move time's not yet fully elapsed -- interpolate position
      int16_t e = ease[255 * dt / eyeMoveDuration] + 1;   // Ease curve
      eyeX = eyeOldX + (((eyeNewX - eyeOldX) * e) / 256); // Interp X
      eyeY = eyeOldY + (((eyeNewY - eyeOldY) * e) / 256); // and Y
    }
  } else {                                // Eye stopped
    eyeX = eyeOldX;
    eyeY = eyeOldY;
    if(dt > eyeMoveDuration) {            // Time up?  Begin new move.
      int16_t  dx, dy;
      uint32_t d;
      do {                                // Pick new dest in circle
        eyeNewX = random(1024);
        eyeNewY = random(1024);

        dx      = (eyeNewX * 2) - 1023;
        dy      = (eyeNewY * 2) - 1023;
    } while((d = (dx * dx + dy * dy)) > (eyeXRange * eyeYRange)); // Keep trying
      eyeNewX += eyeXOffset;
      eyeNewY += eyeYOffset;
      eyeMoveDuration  = random(72000, 144000); // ~1/14 - ~1/7 sec
      eyeMoveStartTime = t;               // Save initial time of move
      eyeInMotion      = true;            // Start move on next frame
    }
  }

  // Iris scaling: remap from 0-1023 input to iris map height pixel units
  iScale = ((IRIS_MAP_HEIGHT + 1) * 1024) /
           (1024 - (iScale * (IRIS_MAP_HEIGHT - 1) / IRIS_MAP_HEIGHT));

  // Scale eye X/Y positions (0-1023) to pixel units used by drawEye()
  eyeX = map(eyeX, 0, 1023, 0, SCLERA_WIDTH  - 128);
  eyeY = map(eyeY, 0, 1023, 0, SCLERA_HEIGHT - 128);
  if(eyeIndex == 1) eyeX = (SCLERA_WIDTH - 128) - eyeX; // Mirrored display

  // Horizontal position is offset so that eyes are very slightly crossed
  // to appear fixated (converged) at a conversational distance.  Number
  // here was extracted from my posterior and not mathematically based.
  // I suppose one could get all clever with a range sensor, but for now...
  if(eyeX > (SCLERA_WIDTH - 128)) eyeX = (SCLERA_WIDTH - 128);

  // Eyelids are rendered using a brightness threshold image.  This same
  // map can be used to simplify another problem: making the upper eyelid
  // track the pupil (eyes tend to open only as much as needed -- e.g. look
  // down and the upper eyelid drops).  Just sample a point in the upper
  // lid map slightly above the pupil to determine the rendering threshold.
  static uint8_t uThreshold = 128;
  uint8_t        lThreshold, n;
  uThreshold = lThreshold = 0;

  // The upper/lower thresholds are then scaled relative to the current
  // blink position so that blinks work together with pupil tracking.
  n          = uThreshold;
  
  // Pass all the derived values to the eye-rendering function:
  drawEye(eyeIndex, iScale, eyeX, eyeY, n, lThreshold);
}

