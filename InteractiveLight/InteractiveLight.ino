#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN A4
#define PIN2 A1
int priorButtonValue = 0;
int mode = 0;
int pixelCount = 55;
//int pixelCount = 60;
bool debugMode = false;
bool micOutput = false;
int rainbowStep = 0;
int soundValues[11];
int soundValuesCount = 0;
int chaseStep = 0;
int chaseColor = 0;
int chaseDirection = 1;
int modeDivisor = 7;
int targetBrightness = 0;
int currentBrightness = 0;


// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strips[2] = {Adafruit_NeoPixel(pixelCount, PIN, NEO_GRB + NEO_KHZ800),Adafruit_NeoPixel(pixelCount, PIN2, NEO_GRB + NEO_KHZ800)};
// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

int heatColors[30] = {
strips[0].Color(255,255,255),strips[0].Color(255,221,150),strips[0].Color(255,221,75),strips[0].Color(255,221,25),strips[0].Color(255,221,0),
strips[0].Color(255,221,0),strips[0].Color(255,220,0),strips[0].Color(255,200,0),strips[0].Color(255,190,0),strips[0].Color(255,183,0),
strips[0].Color(255,179,0),strips[0].Color(255,169,0),strips[0].Color(255,159,0),strips[0].Color(255,149,0),strips[0].Color(255,139,0),
strips[0].Color(255,128,0),strips[0].Color(255,100,0),strips[0].Color(255,80,0),strips[0].Color(255,50,0),strips[0].Color(255,25,0),
strips[0].Color(255,0,0),strips[0].Color(225,0,0),strips[0].Color(200,0,0),strips[0].Color(165,0,0),strips[0].Color(125,0,0),
strips[0].Color(100,0,0),strips[0].Color(75,0,0),strips[0].Color(50,0,0),strips[0].Color(25,0,0),strips[0].Color(0,0,0)
};

int totalHeatValues = 30;
int heatValues[2][55] = {
  {30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
  {30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
};

void randomChange() {
  for (int j = 0; j<=1; j++) {
    for (int i = 0; i<pixelCount; i++) {
      if (i > 0) {
        if (heatValues[j][i-1] > 0) {
          heatValues[j][i] = heatValues[j][i-1] - random(0, 2);
          if (heatValues[j][i] < 0) {
            heatValues[j][i] = 0;
          }
        }
      }
    }
  }
}

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code

  if (debugMode) {
    Serial.begin(9600);
  }
  strips[0].begin();
  strips[0].setBrightness(50);
  strips[0].show(); // Initialize all pixels to 'off'
  strips[1].begin();
  strips[1].setBrightness(50);
  strips[1].show();
  pinMode(1, INPUT_PULLUP);  
  pinMode(A2, INPUT);
  for (int i=0; i<=1; i++) {
    for (int j=30; j>=0; j--) {
      heatValues[i][j] = j; 
    }
  }
  
  for (int i=1; i<pixelCount; i++) {
    heatValues[0][i] = 0;
    heatValues[1][i] = 0;
  }

  //do a test on each strip...
  for (int i=0; i<=1; i++) {
    for (int j=0; j<=55; j++) {
      strips[i].setPixelColor(j,strips[0].Color(0,25,180));
      strips[i].show();
      Serial.println(j);
      delay(50);
    }
    
  }
}

void animateChase(int runStep, int runDirection, int runColor) {
  //if we're going up, then just set the next pixel, if we're going down, unset the previous
  if (runDirection == 1) {
    strips[0].setPixelColor(runStep, runColor);
    strips[1].setPixelColor(runStep, runColor);
  } else {
    strips[0].setPixelColor(runStep+1, strips[0].Color(0,0,0));
    strips[1].setPixelColor(runStep+1, strips[0].Color(0,0,0));
    
  }

  strips[0].show();
  strips[1].show();
}

void loop() {
  // Some example procedures showing how to display to the pixels:
  /*
  colorWipe(strips[0].Color(255, 0, 0), 50); // Red
  colorWipe(strips[0].Color(0, 255, 0), 50); // Green
  colorWipe(strips[0].Color(0, 0, 255), 50); // Blue
//colorWipe(strips[0].Color(0, 0, 0, 255), 50); // White RGBW
  // Send a theater pixel chase in...
  theaterChase(strips[0].Color(127, 127, 127), 50); // White
  theaterChase(strips[0].Color(127, 0, 0), 50); // Red
  theaterChase(strips[0].Color(0, 0, 127), 50); // Blue

  rainbow(20);
  rainbowCycle(20);
  theaterChaseRainbow(50);
  */
  
  int currentButtonValue = analogRead(A0);
  if (priorButtonValue > 400 && currentButtonValue < 10) {
    //button pressed, change mode
    mode++;
    strips[0].fill((0,0,0));
    strips[1].fill((0,0,0));
    strips[0].show();
    strips[1].show();
    currentBrightness = 50;
    targetBrightness = 50;

    if (mode > 8) {
      if (debugMode) {
        Serial.println("Resetting back to mode 0...");
      }
      mode = 0;
    }
    chaseStep = 0;
    chaseDirection = 0;
    Serial.print("Changing Modes to... ");
    Serial.println(mode);
    heatValues[ 0 ][ 0 ] = totalHeatValues;
    heatValues[ 1 ][ 0 ] = totalHeatValues;
  }

  //default mode is OFF
  if (mode == 0) {
    if (debugMode) {
      Serial.println("In mode 0, so resetting and showing 1...");
    }
    strips[0].fill((0,0,0));
    strips[1].fill((0,0,0));
    mode = 1;
    strips[0].show();
    strips[1].show();
  }


  if (micOutput) {
    Serial.println(analogRead(A2));
  }
  //mode 1 does nothing... it is the off state

  //mode 2 is the flame animation
  if (mode == 2) {
    //if the microphone reads a value over 500 (high volume) then greatly increase the heat
    if (analogRead(A2) > 500) {
      for (int i=0; i<=25; i++) {
        for (int j=0; j<=1; j++) {
          if (heatValues[j][i] < 26) {
            heatValues[j][i]=heatValues[j][i]+4;
          }
        }
      }
    }

    //randomly change the brightness
    if (random(0,100) == 1) {
      strips[0].setBrightness(random(30,70));
      strips[1].setBrightness(random(30,70));
    }
    

    //go through each pixel and determine how it should head up/cool down.
    for (int j = 0; j<=1; j++) {
      for (int i = 0; i<pixelCount; i++) {
        if (i>0) {
          if (heatValues[j][i-1] > 0){
            if (debugMode) {
              Serial.print("Checking ");
              Serial.print(j);
              Serial.print(" - ");
              Serial.print(i);
              Serial.print(" has value: ");
              Serial.print(heatValues[j][i]);
              Serial.print(" -- ");
              Serial.println(heatValues[j][i-1]);
            }
            if (heatValues[j][i-1] - heatValues[j][i] > 4) {
              heatValues[j][i] = heatValues[j][i] + 1;
              if (heatValues[j][i-1] > 0 && random(0,5)==1) {
                  heatValues[j][i-1]--;
              }
            } else if  (heatValues[j][i-1] == heatValues[j][i]) {
              if (random(0,50)==1){
                heatValues[j][i]--;
              } else if (random(0,100)==1) {
                heatValues[j][i]++;
              }
            } else {
              int percentChance = random(0,100);
              if (percentChance < 20) {
                heatValues[j][i]++;              
              } else if (percentChance > 70) {
                heatValues[j][i]--;              
              }
            }
          } else {
            if (heatValues[j][i] > 0) {
              heatValues[j][i]--;
            } else {
              heatValues[j][i] = 0;
            }
          }
        }
      }
    }

    //randomly add a spark with a 1% chance
    if (random(0,100) == 1) {
      int randStrip = random(0,1);
      for (int i=0; i<=pixelCount; i++) {
        //look for the first pixel that has no heat - then if it's less than 40, create a small spark 5 up from that...
        if (heatValues[randStrip][i] == 0) {
          if (i<40) {
            heatValues[randStrip][i+5] = 10;
            heatValues[randStrip][i+6] = 8;
            heatValues[randStrip][i+7] = 6;
            heatValues[randStrip][i+8] = 4;
            heatValues[randStrip][i+9] = 2;
            break; // break out of the for loop.
          }
        }
      }
    }

    //set the values to show
    for (int j=0; j<=1; j++) {
      for (int i=0; i<pixelCount; i++) {
        if (heatValues[j][i] < 0) {
          heatValues[j][i] = 0;
        }
        if (heatValues[j][i] >= totalHeatValues) {
          heatValues[j][i] = totalHeatValues-1;
        }
        //strips[j][i] = heatColors[(totalHeatValues-1)-heatValues[j][i]];
        strips[j].setPixelColor(i, heatColors[(totalHeatValues-1)-heatValues[j][i]]);
      }
    }
    strips[0].show();
    strips[1].show();  
    delay(100);
  }

  if (mode == 3) {
    int baseSound = analogRead(A2);
    //Serial.print("Base sound: ");
    //Serial.print(baseSound);
    //Serial.print(" ");
    //Serial.print(baseSound-380);
    //Serial.print(" ");
    //Serial.println(baseSound-380/10);
   
    //int soundLevel = ((baseSound-380)/5);
    soundValues[soundValuesCount] = baseSound;
    soundValuesCount++;
    if (soundValuesCount>10) {
      int totalDiff = 0;
      for (int i=1; i<soundValuesCount; i++) {
        totalDiff += abs(soundValues[i-1]-soundValues[i]);        
      }
      if (currentBrightness > targetBrightness) {
        currentBrightness-=5;
      } else if (currentBrightness < targetBrightness) {
        currentBrightness+=5;
      } else {
        if (totalDiff < 20) {
          targetBrightness = 10;
        } else if (totalDiff < 40) {
          targetBrightness = 20;
        } else if (totalDiff < 75) {
          targetBrightness = 30;
        } else if (totalDiff < 150) {
          targetBrightness = 40;
        } else if (totalDiff < 300) {
          targetBrightness = 50;
        } else if (totalDiff < 500) {
          targetBrightness = 60;
        } else {
          targetBrightness = 70;
        }
      }

      strips[0].setBrightness(currentBrightness);
      strips[1].setBrightness(currentBrightness);
      
      soundValuesCount = 0;
    }
    /*
    Serial.println(soundLevel);
    for(uint16_t i=0; i<strips[0].numPixels(); i++) {
      if (i<soundLevel) {
        strips[0].setPixelColor(i, strips[0].Color(0, 40, 200));        
        strips[1].setPixelColor(i, strips[0].Color(200,40, 0));        
      } else {
        strips[0].setPixelColor(i, strips[0].Color(0, 0, 0));        
        strips[1].setPixelColor(i, strips[0].Color(0, 0, 0));                
      }
    }  
    */
    rainbowAnimationStep(rainbowStep);
    rainbowStep++;
    if (rainbowStep > 255) {
      rainbowStep =0;
    }
    
    strips[0].show();
    strips[1].show();
    delay(10);
  }

  //do light chasers with different color for the next few modes.
  if (mode == 4) {
    chaseColor = strips[0].Color(255,0,0);
  }
  if (mode == 5) {
    chaseColor = strips[0].Color(0,255,0);
  }
  if (mode == 6) {
    chaseColor = strips[0].Color(0,0,255);
  }
  if (mode == 7) {
    chaseColor = strips[0].Color(255,255,255);
  }

  if (mode == 4 || mode == 5 || mode == 6 || mode == 7) {
    chaseStep = chaseStep + chaseDirection;
    if (chaseStep%modeDivisor == 0) {
      animateChase(chaseStep/modeDivisor, chaseDirection, chaseColor);
    }

    if (chaseStep == modeDivisor*pixelCount) {
      chaseDirection = -1;
    }
    if (chaseStep == 0) {
      chaseDirection = 1;
    }
    delay(10);
  }

/*
  Serial.print("Button: ");
  Serial.print(analogRead(A0));
  Serial.print(" Microphone: ");
  Serial.print(analogRead(A2));
  Serial.println();
  */
  priorButtonValue = currentButtonValue;
  //delay(10);
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strips[0].numPixels(); i++) {
    strips[0].setPixelColor(i, c);
    strips[0].show();
    strips[1].setPixelColor(i, c);
    strips[1].show();
    delay(wait);
  }
}

void rainbowAnimationStep(int stepNum) {
  for(int i=0; i< strips[0].numPixels(); i++) {
    strips[0].setPixelColor(i, Wheel(((i * 256 / strips[0].numPixels()) + stepNum) & 255));
    strips[1].setPixelColor(i, Wheel(((i * 256 / strips[1].numPixels()) + (stepNum+50)) & 255));
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strips[0].numPixels(); i++) {
      strips[0].setPixelColor(i, Wheel((i+j) & 255));
    }
    strips[0].show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strips[0].numPixels(); i++) {
      strips[0].setPixelColor(i, Wheel(((i * 256 / strips[0].numPixels()) + j) & 255));
    }
    strips[0].show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strips[0].numPixels(); i=i+3) {
        strips[0].setPixelColor(i+q, c);    //turn every third pixel on
      }
      strips[0].show();

      delay(wait);

      for (uint16_t i=0; i < strips[0].numPixels(); i=i+3) {
        strips[0].setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strips[0].numPixels(); i=i+3) {
        strips[0].setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
      }
      strips[0].show();

      delay(wait);

      for (uint16_t i=0; i < strips[0].numPixels(); i=i+3) {
        strips[0].setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strips[0].Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strips[0].Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strips[0].Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
