// A basic everyday NeoPixel strip test program.

// NEOPIXEL BEST PRACTICES for most reliable operation:

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN    1

#define BUTTON_PIN 3

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 8

int previousButtonValue = 1;
int currentButtonValue = 1;
int mode = 0;
int colorDirection = 1;
int currentBrightness = 40;
int animationFrame = 0;
int subAnimation = 0;
int subAnimationCounter = 0;
int subAnimationLoop = 0;
int subAnimationColor = 0;

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)


// setup() function -- runs once at startup --------------------------------

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  Serial.begin(9600);
  

  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.fill(strip.Color(0,0,0));
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(40); // Set BRIGHTNESS to about 1/5 (max = 255)

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  colorWipe(strip.Color(255,   0,   0), 200); // Red
  colorWipe(strip.Color(  255, 255,   0), 200); // Green
  colorWipe(strip.Color(  0,   255, 0), 200); // Blue
}


// loop() function -- runs repeatedly as long as board is on ---------------

void loop() {
  // Fill along the length of the strip in various colors...
  currentButtonValue = digitalRead(BUTTON_PIN);
  if (currentButtonValue == 0 && previousButtonValue == 1) {
    //change mode
    mode++;
    strip.fill(strip.Color(0,0,0));
    strip.show();
    if (mode > 6) {
      mode = 0;
    }
  }

  if (mode == 0) {
    strip.fill(strip.Color(0,0,0));
    strip.show();
  }

  if (mode == 1) {
    strip.fill(strip.Color(255,255,255));
    currentBrightness+=colorDirection;
    strip.setBrightness(currentBrightness);
    if (currentBrightness == 80) {
      colorDirection = -1;
    } else if (currentBrightness == 20) {
      colorDirection = 1;
    }
    strip.show();
    delay(40);
  }

  if (mode == 2) {
    strip.fill(strip.Color(0,0,255));
    currentBrightness+=colorDirection;
    strip.setBrightness(currentBrightness);
    if (currentBrightness == 80) {
      colorDirection = -1;
    } else if (currentBrightness == 10) {
      colorDirection = 1;
    }
    strip.show();
    delay(35);
  }
  if (mode == 3) {
    strip.fill(strip.Color(204,0,204));
    currentBrightness+=colorDirection;
    strip.setBrightness(currentBrightness);
    if (currentBrightness == 80) {
      colorDirection = -1;
    } else if (currentBrightness == 10) {
      colorDirection = 1;
    }
    strip.show();
    delay(35);
  }
  if (mode == 4) {
    strip.fill(strip.Color(255,0,0));
    currentBrightness+=colorDirection;
    strip.setBrightness(currentBrightness);
    if (currentBrightness == 80) {
      colorDirection = -1;
    } else if (currentBrightness == 10) {
      colorDirection = 1;
    }
    strip.show();
    delay(35);
  }

  if (mode == 5)  {
    rainbow(20, animationFrame);
    animationFrame++;
    if (animationFrame > 1279) {
      animationFrame = 0;
    }
  }

  if (mode == 6) {
    //this will do random animations.  Mostly be off, but will cycle through a few things
    //that are somewhat clock related.
    //int subAnimation = 0;
    //int subAnimationCounter = 0;
    //int subAnimationLoop = 0;
    //subAnimationColor

    subAnimationCounter++;
    //if (subAnimationCounter > 3000) { //50 = 1s 60s = 3000
    if (subAnimationCounter > 600) { //50 = 1s 60s = 3000
      subAnimation = random(0,10);
      subAnimationCounter = 0;
      subAnimationLoop = 0;
      subAnimationColor = strip.Color(random(0,255),random(0,255), random(0,255));
      strip.fill(0,0,0);
      strip.show();
    }

    //pulse
    if (subAnimation == 1) {
      if (subAnimationCounter<255) {
        strip.fill(strip.Color(subAnimationCounter,subAnimationCounter,subAnimationCounter));
      } else if (subAnimationCounter < 512) {
        strip.fill(strip.Color(512-subAnimationCounter,512-subAnimationCounter,512-subAnimationCounter));        
      } else {
        strip.fill(strip.Color(0,0,0));
      }
      strip.show();
    }
    
    //tick-tock (random color)
    if (subAnimation == 2) {
      strip.fill(strip.Color(0,0,0));
      int step1 = round(subAnimationCounter/50)%8;
      int step2 = 0;
      if (step1 < 4) {
        step2 = step1+4;
      } else {
        step2 = step1-4;
      }
      strip.setPixelColor(step1,subAnimationColor);
      strip.setPixelColor(step2,subAnimationColor);
      strip.show();
    }
    
    //tick-tock (random color) reverse
    if (subAnimation == 3) {
      strip.fill(strip.Color(0,0,0));
      int step1 = 7-(round(subAnimationCounter/50)%8);
      int step2 = 0;
      if (step1 < 4) {
        step2 = step1+4;
      } else {
        step2 = step1-4;
      }
      strip.setPixelColor(step1,subAnimationColor);
      strip.setPixelColor(step2,subAnimationColor);
      strip.show();
    }

    //top-down wipe (random color)
    if (subAnimation == 4) {
      strip.fill(strip.Color(0,0,0));
      int step1 = round(subAnimationCounter/50);
      if (step1 == 1) {
        strip.setPixelColor(7,subAnimationColor);        
      } else if (step1 == 2) {
        strip.setPixelColor(7,subAnimationColor);        
        strip.setPixelColor(6,subAnimationColor);        
        strip.setPixelColor(0,subAnimationColor);        
      } else if (step1 == 3) {
        strip.setPixelColor(7,subAnimationColor);        
        strip.setPixelColor(6,subAnimationColor);        
        strip.setPixelColor(0,subAnimationColor);        
        strip.setPixelColor(5,subAnimationColor);        
        strip.setPixelColor(1,subAnimationColor);        
      } else if (step1 == 4) {
        strip.setPixelColor(7,subAnimationColor);        
        strip.setPixelColor(6,subAnimationColor);        
        strip.setPixelColor(0,subAnimationColor);        
        strip.setPixelColor(5,subAnimationColor);        
        strip.setPixelColor(1,subAnimationColor);        
        strip.setPixelColor(4,subAnimationColor);        
        strip.setPixelColor(2,subAnimationColor);        
      } else if (step1 == 5) {
        strip.fill(subAnimationColor);        
      }
      strip.show();
    }
    
  }

  delay(20);
  // Do a theater marquee effect in various colors...
  previousButtonValue = currentButtonValue;
}


// Some functions of our own for creating animated effects -----------------

// Fill strip pixels one after another with a color. Strip is NOT cleared
// first; anything there will be covered pixel by pixel. Pass in color
// (as a single 'packed' 32-bit value, which you can get by calling
// strip.Color(red, green, blue) as shown in the loop() function above),
// and a delay time (in milliseconds) between pixels.
void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

// Theater-marquee-style chasing lights. Pass in a color (32-bit value,
// a la strip.Color(r,g,b) as mentioned above), and a delay time (in ms)
// between frames.
void theaterChase(uint32_t color, int wait) {
  for(int a=0; a<10; a++) {  // Repeat 10 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in steps of 3...
      for(int c=b; c<strip.numPixels(); c += 3) {
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
    }
  }
}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait, int animationFrame) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  long firstPixelHue = animationFrame * 256;
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    // Offset pixel hue by an amount to make one full revolution of the
    // color wheel (range of 65536) along the length of the strip
    // (strip.numPixels() steps):
    int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
    // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
    // optionally add saturation and value (brightness) (each 0 to 255).
    // Here we're using just the single-argument hue variant. The result
    // is passed through strip.gamma32() to provide 'truer' colors
    // before assigning to each pixel:
    strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
  }
  strip.show(); // Update strip with new contents
  delay(wait);  // Pause for a moment
}

// Rainbow-enhanced theater marquee. Pass delay time (in ms) between frames.
void theaterChaseRainbow(int wait) {
  int firstPixelHue = 0;     // First pixel starts at red (hue 0)
  for(int a=0; a<30; a++) {  // Repeat 30 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in increments of 3...
      for(int c=b; c<strip.numPixels(); c += 3) {
        // hue of pixel 'c' is offset by an amount to make one full
        // revolution of the color wheel (range 65536) along the length
        // of the strip (strip.numPixels() steps):
        int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
        uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show();                // Update strip with new contents
      delay(wait);                 // Pause for a moment
      firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
    }
  }
}
