/*
 * Pong-playing suspenders (with a few other animations!)
 * This code will control a circuit playground (or other arduino-compatible device) 
 * and control 2 strips of LEDs with 2 buttons, one a pressure sensor, one a button,
 * although either could be swapped with a different input with minimal code.
 * 
 * Much of this was from the Adafruit Neopixel "Strip Test" library.  I kept much of 
 * it in case you wish to use a non-circuit-playground device,
 * but, as it stands, there is certainly unnecessary code in here.
 */
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#include <Adafruit_CircuitPlayground.h>

//Define the button pin
#define buttonPin A1

//define the number of pixels on each strip
int numPixels = 72;

//set up an array of 2 different strips.  My version has 72 pixels, you can adjust that above.
//I used WS2812B 5050 RGB LEDs.  They are rated at 5V but work well enough at 3.3V
Adafruit_NeoPixel strip[2] = {
    Adafruit_NeoPixel(numPixels, A2, NEO_GRB + NEO_KHZ800),
    Adafruit_NeoPixel(numPixels, A5, NEO_GRB + NEO_KHZ800)
};

boolean activeAnimation = false;
bool leftButtonPressed;
bool rightButtonPressed;
int buttonState = 0;
int mode = 0;
int buttonWait = 0;

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  /*
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  */
  // End of trinket special code

  //Serial for debugging.  Remove for higher performance code.
  Serial.begin(9600);  
  Serial.println("Starting...");

  CircuitPlayground.begin();
  //Initiate the strips
  strip[0].begin();
  strip[0].setBrightness(10);
  strip[0].show(); // Initialize all pixels to 'off'

  strip[1].begin();
  strip[1].setBrightness(10);
  strip[1].show(); // Initialize all pixels to 'off'
  
  //initiate the buttonPin as an input
  pinMode(buttonPin, INPUT);
}

/*
 * This function fills pixels from the bottom of the strip to the top.  Since the first pixel is
 * closest to the device, and therefore at the top of the suspenders, it starts at the
 * last pixel and works it's way up.
 */
void fillFromBottom(int x) {
  for(uint16_t i=0; i<numPixels; i++) {
    for (int j=0; j<=1; j++) {
      if (numPixels-i <= x) {
        strip[j].setPixelColor(numPixels-i, strip[0].Color(0,200,0));
      } else {
        strip[j].setPixelColor(numPixels-i, strip[0].Color(0,0,0));
      }
    }
  }
  strip[0].show();
  strip[1].show();
}


/* This function is no longer played, as it was very slow, but it played a "star"
 *  type animation - having one pixel fade in, then fade out...  Leaving here in case someone wants to use it.
 */
void playStarAnimation() {
  int previous_pixel = 0;
  int previous_strip = 0;
  for (uint16_t i=0; i<16; i++) {
    int pixel_num = random(0, (numPixels*2)-1);
    int strip_num = 0;
    
    if (pixel_num >= numPixels) {
       strip_num++;
       pixel_num = pixel_num - numPixels; 
    }

    strip[previous_strip].setPixelColor(previous_pixel, 0,0,0);

    for (uint16_t i=0; i<=63; i++) {
       strip[strip_num].setPixelColor(pixel_num, i*4,i*4,i*4);      
       strip[strip_num].show();
       delay(3);
    }
    for (uint16_t i=63; i>0; i--) {
       strip[strip_num].setPixelColor(pixel_num, i*4,i*4,i*4);      
       strip[strip_num].show();
       delay(3);
    }
    
    strip[0].show();
    strip[1].show();
    previous_pixel = pixel_num;
    previous_strip = strip_num;
    delay(200);
  }
  resetStrips();
}


/*
 * This function causes the suspenders to sparkle.
 */
void playGlitterAnimation() {

  //Repeat this animation 100 times.
  for (int k=0; k<=100; k++) {
    //for each strip (0 and 1) run the animation
    for (int j=0; j<=1; j++) {
      //Go through each pixel, and pick a random number.  A 1 in 6 chance the pixel will be white,
      //otherwise black.  This causes things to flash quickly and give a neat sparkle effect.
      for (uint16_t i=0; i<numPixels; i++) {
        int randSeed = random(1,6);
        if (randSeed == 1) {
          strip[j].setPixelColor(i,255,255,255);
        } else {
          strip[j].setPixelColor(i,0,0,0);        
        }
      }
      strip[j].show();
    }
    delay(50); // delay 50ms.  You can increase/decrease this to change the effect
  }
  resetStrips(); // return the strips to all black.
}

/*
 * This function allows the suspenders to play pong.  It will continue the game of pong until a single player scores a point,
 * at which point, their side lights green, and the opponent's side lights red, then the game is over.
 */
void playPong() {
  //reset the strips to all-black
  resetStrips();

  //set the game as "on" so that it will run through game code
  bool gameOn = true;

  //initialize the variables needed
  int winner = 0; // this is the strip # of the winner
  int loser = 0; // this is the strip # of the loser
  int ballDirection = 1; // ball direction is a multiplier to move the ball in a + or - direction (towards one player or another)
  int ballPosition = 0; // the position on the virtual line.  Ultimately the line is a join of the two strips
  int gameDelay = 16; // the starting delay - the MS between each animation.  If you use a really fast processor, you might want to increase this.

  //pick a random start direction.  It's 1,3 because it picks a number BETWEEN 1 and 3, so basically 1 or 2...
  if (random(1,3) == 1) {
    ballDirection = -1;
  }

  //while the game is active, continue in the game loop.  
  while (gameOn) {
    //set the pixel that will mark the two lines when the user can bounce the ball
    strip[0].setPixelColor(numPixels-4,0,0,200);
    strip[1].setPixelColor(numPixels-4,0,0,200);

    //move the ball
    int ballPreviousPosition = ballPosition;
    ballPosition = ballPosition + ballDirection;

    //the ball position is + if on the left side, - if on the right side, that's how the line
    //is managed, so make sure to set the appropriate pixel to WHITE, and the previous
    //position to BLACK.
    if (ballPosition < 0) {
      strip[0].setPixelColor(-ballPosition,255,255,255);
    } else {
      strip[1].setPixelColor(ballPosition,255,255,255);      
    }
    if (ballPreviousPosition < 0) {
      strip[0].setPixelColor(-ballPreviousPosition,0,0,0);
    } else {
      strip[1].setPixelColor(ballPreviousPosition,0,0,0);      
    }
    

    strip[1].show();
    strip[0].show();

    //delay the game a bit - to slow the animation
    if (gameDelay > 1)  {
      delay(gameDelay);
    }
    
    //check for a hit
    //The -4 is checking that the ball is within 4 pixels of the bottom, giving the user time to react
    if (ballPosition < (-(numPixels - 4)) && ballDirection == -1) {
      buttonState = digitalRead(buttonPin);
      if (buttonState ==1) {
        ballDirection = 1; // make the ball go in the opposite direction
        gameDelay = gameDelay -1; //reduce the delay, making the ball go faster
      }       
    } else if (ballPosition > (numPixels - 4) && ballDirection == 1) {
      float resist = analogRead(A6);
      Serial.print("Resist: ");
      Serial.println(resist);
      if (resist > 100) {
        ballDirection = -1; // make the ball go in the opposite direction
        gameDelay = gameDelay - 1; //reduce the delay, making the ball go faster
      }
    }

    //check for win condition of one player
    if (ballDirection == -1 && (ballPosition + ballDirection <= -numPixels)) {
      gameOn = false;
      winner = 1;
      loser = 0;
    }
    //check for a win condition of the 2nd player
    if (ballDirection == 1 && (ballPosition + ballDirection >= numPixels)) {
      gameOn = false;
      winner = 0;
      loser = 1;      
    }

  }

  //set the winner's strip as green, the loser's strip as red
  //for some reason the .fill() function wasn't working, so I manually set each pixel color
  for (int j = 0; j<numPixels; j++) {
    strip[winner].setPixelColor(j, 0,255,0);
    strip[loser].setPixelColor(j,255,0,0);
  }
  
  //show both strips for 3 seconds to provide feedback then reset back to the default position
  strip[0].show();
  strip[1].show();
  
  delay(3000);
  resetStrips();
}

/*
 * Reset the strips to all black
 */
void resetStrips() {
  strip[0].fill(0,0,0);
  strip[1].fill(0,0,0);
  strip[0].show();
  strip[1].show();  
}


/*
 * Main Loop - will check for button presses and call animations
 */
void loop() {

  //variables for the buttons on the circuit playground being pressed.  These are used for debugging.
  leftButtonPressed = CircuitPlayground.leftButton();
  rightButtonPressed = CircuitPlayground.rightButton();

  //get the state of the button
  buttonState = digitalRead(buttonPin);
  
  //Check to see if the left or right button have been pressed on the CPX and light up the strip
  if (leftButtonPressed) {
    //Serial.print("DOWN");
    rainbow(0.001,0);
    resetStrips();
  }

  if (rightButtonPressed) {
    //Serial.print("DOWN");
    rainbow(0.001,1);
    activeAnimation = false;
    resetStrips();
  }

  //buttonWait acts as a delay of button presses.  I only wanted a click to register when first pressed.
  //this allows a click to be registered one out of every 10,000 loops, which was about 3-4 seconds on
  //the CircuitPlayground Express.  This keeps the variable from getting too high and overflowing or
  //running unnecessary computations constantly.
  if (buttonWait<=10000) {
    buttonWait++;
  }

  // if the button was pressed, and enough time passed since the last button press, advance to the next mode 
  if (buttonWait >= 1000 && buttonState == 1) {
    buttonWait = 0;
    mode++;
    //check to see if we're at the top mode, if so, loop to the bottom
    if (mode > 3) {
       mode = 0;
    }
  }
  //get the valid of the pressure sensor (essentially used as a button)
  float resist = analogRead(A6);
  float multiplier = 0;

  //if the resistor value is greater than 50, which is a "light tap" you can adjust this but I found it reasonable.
  if (resist > 50) {
    switch (mode) {
      case 0: // pong
        playPong();
        break;

      case 1: //Pressure
        multiplier = (resist-50)/(1024-50);
        fillFromBottom((int)numPixels*multiplier);
        break;
      case 2: // Glitter
        playGlitterAnimation();
        break;
      case 3: // Rainbow
        rainbowCycle(2);
        resetStrips();
        break;
        /* Removed as they were for demo purposes
      case 1: // Stars
      //Serial.println("About to run Star Animation");
        Serial.println("STAR GO!");
        playStarAnimation();      
        break;
      case 4: // tilt
        multiplier = (CircuitPlayground.motionZ()+9.8 / 18);
        if (multiplier <0) {
          multiplier = 0;
        } else if (multiplier > 1) {
          multiplier = 1;
        }

        fillFromBottom((int)numPixels*multiplier);
        break;

      */
    }
  }

    delay(1);

}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip[0].numPixels(); i++) {
    for (int i=0; i<=1; i++) {
      strip[i].setPixelColor(i, c);
      strip[i].show();
      delay(wait);
    }
  }
}

/* created by Adafruit as part of the striptest library - runs colors through a rainbow animation */
void rainbow(uint8_t wait, uint8_t stripnum) {
  uint16_t i, j, k;

  for(j=0; j<256; j++) {
    for(i=0; i<strip[0].numPixels(); i++) {
      strip[stripnum].setPixelColor(i, Wheel((i+j) & 255));
    }
    strip[stripnum].show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*4; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip[0].numPixels(); i++) {
      for (int k=0; k<=1; k++) {
        strip[k].setPixelColor(i, Wheel(((i * 256 / strip[0].numPixels()) + j) & 255));
      }
    }
    strip[0].show();
    strip[1].show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip[0].numPixels(); i=i+3) {
        for (int k=0; k<=1; k++) {
          strip[k].setPixelColor(i+q, c);    //turn every third pixel on
        }
      }
      strip[0].show();
      strip[1].show();

      delay(wait);

      for (uint16_t i=0; i < strip[0].numPixels(); i=i+3) {
        for (int k=0; k<=1;k++){
          strip[k].setPixelColor(i+q, 0);        //turn every third pixel off
        }
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip[0].numPixels(); i=i+3) {
        for (int k=0; k<=1; k++) {
          strip[k].setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
        }
      }
      strip[0].show();
      strip[1].show();

      delay(wait);

      for (uint16_t i=0; i < strip[0].numPixels(); i=i+3) {
        for (int k=0; k<=1; k++) {
          strip[k].setPixelColor(i+q, 0);        //turn every third pixel off
        }
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip[0].Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip[0].Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip[0].Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
