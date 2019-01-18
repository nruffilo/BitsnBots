#include <Adafruit_CircuitPlayground.h>

#include <Adafruit_NeoPixel.h>
#define PIN 6

#define NUM_LEDS 13

#define BRIGHTNESS 255
#define FRAME_LOOP 16

uint16_t mode = 0;
uint16_t lightSensorValue = 0;
uint16_t noiseLevel = 0;
uint16_t loopCounter = 0;
uint16_t currentLightLevel = 0;
uint16_t previousLightLevel = 0;
uint8_t animationSequence = 0;
uint8_t animationFrame = 0;
int value;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);  
  // put your setup code here, to run once:
  // End of trinket special code
  strip.setBrightness(BRIGHTNESS);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  Serial.println("Getting started!");
}

void loop() {
  //Originally, the animations would play fully in loops, but I want to be able to change animations
  //based on sensor values, so I'm going to used framed animation techniques.
  //The animations will tick every few frames, which will let the program check sensor values
  //frequently

  //listen to the mic for 10 milliseconds, this will actually act as a good
  //loop delay
  noiseLevel = CircuitPlayground.mic.soundPressureLevel(10); 

  //Mode 0 - Ambient light is high, no animations, reacts to claps
  //Mode 1 - low ambient light, plays one round of animations then goes to mode 2...
  //Mode 2 - an animation then a low glow.

  //Based on the senors, lets see if we should be changing the mode...
  //Serial.println(CircuitPlayground.lightSensor());
  //value = CircuitPlayground.lightSensor();
  value = analogRead(A5);
  //if (CircuitPlayground.lightSensor() <= 1) {
  if (value < 1) {
    if (mode == 0) {
      Serial.println("Setting to mode 1...");
      mode = 1;
      strip.setBrightness(255);
      loopCounter = 0;
      animationSequence = 1;
      animationFrame = 0;
    }
  } else {
    if (mode == 2 && loopCounter > 0) {
      Serial.println("Clearing up animations after pulse...");
      loopCounter = 0;
      pulseWhite(5);
    } else if(mode==2) {
      mode = 0;
    }  
  }

  //If a loud noise is played - we want to play a specific animation, then continue with everything....
  if (noiseLevel > 80 && mode == 0) {
    Serial.println(noiseLevel);
    pulseWhite(5);
  }

  if (mode == 1) {
    loopCounter++;
    if (loopCounter > 2000) {
      Serial.println("Entering mode 2...");
      Serial.println(loopCounter);
      mode = 2; //if we've run a few frames of animation, set the mode to 2...
    }

    //see which sequence we should be displaying
    if (animationSequence == 1) {
      //the first animation is going to be a flare in.  The outside ones fade in, then the middle flanks, then the center.
      if (loopCounter < 125) {
        if (loopCounter == 0) Serial.println("Mode 1 animation 1");
        strip.setPixelColor(0, strip.Color(loopCounter*2, loopCounter/2, loopCounter/2));
        strip.setPixelColor(1, strip.Color(loopCounter*2, loopCounter/2, loopCounter/2));
        strip.setPixelColor(11, strip.Color(loopCounter*2, loopCounter/2, loopCounter/2));
        strip.setPixelColor(12, strip.Color(loopCounter*2, loopCounter/2, loopCounter/2));
        strip.show();
      } else if (loopCounter <255) {
        if (loopCounter == 126) Serial.println("Mode 1 animation 2");
        int offset = loopCounter-125;
        strip.setPixelColor(2, strip.Color(offset/2, offset*2, offset*2));
        strip.setPixelColor(3, strip.Color(offset/2, offset*2, offset*2));
        strip.setPixelColor(9, strip.Color(offset/2, offset*2, offset*2));
        strip.setPixelColor(10, strip.Color(offset/2, offset*2, offset*2));
        strip.show();
      } else if (loopCounter < (255+64)) {
        if (loopCounter == 255) Serial.println("Mode 1 animation 3");
        int offset = loopCounter - 255;
        for (int j = 4; j<=8; j++) {
          strip.setPixelColor(j, strip.Color(offset*4, 0, offset*4));
        }
        strip.show();
      } else if (loopCounter < 255+(64*2)) {
        if (loopCounter == (255+64)) Serial.println("Mode 1 animation 4");
        int offset = loopCounter - 255-(64*1);
        for (int j = 4; j<=8; j++) {
          strip.setPixelColor(j, strip.Color(0,offset*4, 0));
        }
        strip.show(); 
      } else if (loopCounter < 255+(64*3)) {
        if (loopCounter == 255+(64*2)) Serial.println("Mode 1 animation 5");
        int offset = loopCounter - 255-(64*2);
        for (int j = 4; j<=8; j++) {
          strip.setPixelColor(j, strip.Color(0,0,offset*4));
        }
        strip.show();
      } else {
        Serial.println("Mode 1 animation sequence 2");

        animationSequence = 2;
      }
    } else if (animationSequence == 2) {

      //this will be a bit of a color chase 
      int color_offset = loopCounter - 255 - (64*3);
      for (int j = 0; j<=NUM_LEDS; j++) {
        int setColor = color_offset - (j*10);
        if (setColor<0) setColor = 0;
        if (setColor>255) setColor = 255;
        strip.setPixelColor(j, strip.Color(0,0,setColor));
      }
      strip.show();
      if (color_offset == 400) {
        Serial.println("Loading sequence 3...");
        Serial.print("LoopCounter: ");
        Serial.println(loopCounter);
        animationSequence = 3;        
      }
    } else if (animationSequence == 3) {
      //a lightning like animation
      int color_offset = loopCounter - 847;
      for (int j = 0; j<=NUM_LEDS; j++) {
        int setColor = color_offset - (j*10);
        if (setColor<0) setColor = 0;
        if (setColor>255) setColor = 255;
        strip.setPixelColor(j, strip.Color(0,setColor,setColor));
      }
      strip.show();

    }
  }
  /*
  if (mode == 0) {
    colorWipe(strip.Color(255,255,255),50);
    colorWipe(strip.Color(0,255,255),50);
  } else if (mode == 1) {
    rainbowFade2White(100,3,2);
    pulseWhite(5);
  }
  */
}


void pulseWhite(uint8_t wait) {
  for(int j = 0; j < 126 ; j++){
      for(uint16_t i=0; i<strip.numPixels(); i++) {
          strip.setPixelColor(i, strip.Color(j*2,j*2,j*2) );
        }
        delay(wait);
        strip.show();
      }

  for(int j = 125; j >= 0 ; j--){
      for(uint16_t i=0; i<strip.numPixels(); i++) {
          strip.setPixelColor(i, strip.Color(j*2,j*2,j*2 ) );
        }
        delay(wait);
        strip.show();
      }
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
