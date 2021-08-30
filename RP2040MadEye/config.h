// Pin selections are based on a raspberry pi pico using the bottom half of the board.

// GRAPHICS SETTINGS (appearance of eye) -----------------------------------

// Code is based on a single eye
// uses a simpler "football-shaped" eye that's left/right symmetrical.
// Default shape includes the caruncle, creating distinct left/right eyes.
#define SYMMETRICAL_EYELID

// Enable ONE of these #includes -- HUGE graphics tables for various eyes:
#include "graphics/defaultEye.h"    // Standard human-ish hazel eye -OR-
//#include "graphics/dragonEye.h"   // Slit pupil fiery dragon/demon eye -OR-
//#include "graphics/noScleraEye.h" // Large iris, no sclera -OR-
//#include "graphics/goatEye.h"     // Horizontal pupil goat/Krampus eye -OR-
//#include "graphics/newtEye.h"     // Eye of newt


// EYE LIST ----------------------------------------------------------------

// This table contains ONE LINE PER EYE.  The table MUST be present with
// this name and contain ONE OR MORE lines.  Each line contains THREE items:
// a pin number for the corresponding TFT/OLED display's SELECT line, a pin
// pin number for that eye's "wink" button (or -1 if not used), and a screen
// rotation value (0-3) for that eye.

eyeInfo_t eyeInfo[] = {
  { 20, 2 }, // SINGLE EYE display-select and wink pins, rotate 180
};

// DISPLAY HARDWARE SETTINGS (screen type & connections) -------------------

//#include <Adafruit_SSD1351.h>  // OLED display library -OR-
#include <Adafruit_ST7735.h> // TFT display library (enable one only)
#define TFT_DC        20    // Data/command pin for ALL displays
#define TFT_RESET     13    // Reset pin for ALL displays
#define TFT_CS        21
#define TFT_MOSI      12  // Data out
#define TFT_SCLK      10  // Clock out
#define TFT_HEIGHT    124
#define TFT_WIDTH     124

//pick the speed that seems to work with your device.
#define SPI_FREQ 24000000    // TFT: use max SPI (clips to 12 MHz on M0)
//#define SPI_FREQ 12000000    // TFT: use max SPI (clips to 12 MHz on M0)

// INPUT SETTINGS (for controlling eye motion) -----------------------------

#define IRIS_SMOOTH         // If enabled, filter input from IRIS_PIN
#define IRIS_MIN      120 // Iris size (0-1023) in brightest light
#define IRIS_MAX      520 // Iris size (0-1023) in darkest light

//Adjust these offsets and ranges if inside a mask or skull eye socket
#define eyeXOffset      0 // aim offset on x for autonomous move, default 0
#define eyeYOffset      0  // aim offset on y, default 0
#define eyeXRange       600  // Range of motion on x, full range is 1023
#define eyeYRange       600  // Range of motion on y, full range is 1023
