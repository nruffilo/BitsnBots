import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import random
import math
print("loading")

# ----------------------------
# Hardware / strip config
# ----------------------------
PIXELS_PIN = board.GP0
BTN_PIN = board.GP1
PIXEL_COUNT = 7

# We keep NeoPixel brightness at 1.0 and do brightness in color math.
pixels = neopixel.NeoPixel(PIXELS_PIN, PIXEL_COUNT, brightness=0.8, auto_write=False)

# ----------------------------
# Frame timing (steady clock)
# ----------------------------
TARGET_FPS = 60
FRAME = 1.0 / TARGET_FPS
next_frame = time.monotonic()

# ----------------------------
# Button (debounced edge)
# ----------------------------
btn = DigitalInOut(BTN_PIN)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

last_btn_val = True
debounce_until = 0.0

# Modes: 0=fire, 1=rainbow, 2=comet, 3=meditation, 4..8=fixed fills, 9=chase
animationMode = 0

def update_button():
    """Debounce and advance mode on falling edge."""
    global last_btn_val, debounce_until, animationMode
    now = time.monotonic()
    v = btn.value  # True when not pressed (pull-up), False when pressed
    if now >= debounce_until:
        if last_btn_val and not v:  # falling edge
            animationMode = (animationMode + 1) % 10
            debounce_until = now + 0.15  # 150ms
            # print("Mode:", animationMode)
    last_btn_val = v

# ----------------------------
# Color helpers (int math)
# ----------------------------
# Gamma table greatly improves perceived smoothness.
GAMMA = bytearray(256)
for i in range(256):
    GAMMA[i] = int((i / 255.0) ** 2.6 * 255 + 0.5)

def gamma_rgb(rgb):
    r, g, b = rgb
    return (GAMMA[r], GAMMA[g], GAMMA[b])

def scale_rgb(rgb, bri):  # bri: 0..255
    r, g, b = rgb
    return ((r * bri) // 255, (g * bri) // 255, (b * bri) // 255)

# Precompute wheel (optionally gamma-corrected)
WHEEL = [(0, 0, 0)] * 256
for i in range(256):
    if i < 85:
        WHEEL[i] = (255 - i * 3, i * 3, 0)
    elif i < 170:
        j = i - 85
        WHEEL[i] = (0, 255 - j * 3, j * 3)
    else:
        j = i - 170
        WHEEL[i] = (j * 3, 0, 255 - j * 3)
# Apply gamma to wheel entries:
WHEEL = [gamma_rgb(c) for c in WHEEL]

def fill_const(rgb):
    col = gamma_rgb(rgb)
    for i in range(PIXEL_COUNT):
        pixels[i] = col

# ----------------------------
# Simple stepper utilities
# ----------------------------
class Stepper:
    """Advances an integer position 0..255 at a rate * speed * dt."""
    def __init__(self, speed=0.4):
        self.val = 0
        self.speed = speed  # "cycles per second" through 0..255
    def advance(self, dt):
        # Convert speed (cycles/s) to 0..255 steps per second
        inc = int(self.speed * 256 * dt)
        if inc <= 0:
            inc = 1  # ensure progress even on low dt
        self.val = (self.val + inc) & 255
        return self.val

# ----------------------------
# Animation state
# ----------------------------

# 1) Rainbow
rainbow_stepper = Stepper(speed=0.4)  # tweak slower/faster hue

def rainbow_step():
    idx = rainbow_stepper.advance(dt) 
    # spacing tuned to look good on tiny 7px ring/strip
    stride = 256 // 10
    for i in range(PIXEL_COUNT):
        pixels[i] = WHEEL[(idx + i * stride) & 255]

# 2) Meditation: palette crossfade + breathing brightness (all integer)
# ----- Meditation: 3-color crossfade, brightness shaped (75% -> 33% -> 75%), 4×/min -----

# Palette (unchanged)
PALETTE = [(200, 200, 200), (0, 200, 120), (0, 50, 220)]

# Brightness in 0..255 (≈33% and ≈75%)
MED_BRI_MIN = 85    # ~0.33 * 255
MED_BRI_MAX = 191   # ~0.75 * 255
MED_BRI_RANGE = MED_BRI_MAX - MED_BRI_MIN

class PhaseStepper:
    """Continuous 0..1 phase stepper (float), cycles_per_sec controls speed."""
    def __init__(self, cycles_per_sec):
        self.phase = 0.0
        self.cps = cycles_per_sec  # cycles per second
    def advance(self, dt):
        self.phase += self.cps * dt
        if self.phase >= 1.0:
            self.phase -= int(self.phase)  # keep in [0,1)
        return self.phase

# 4 cycles per minute = 4/60 cycles per second
med_phase = PhaseStepper(cycles_per_sec=(4.0/100.0))

def meditation_step(dt):
    # 1) advance phase 0..1
    ph = med_phase.advance(dt)         # 0..1
    segf = ph * 3.0                    # 0..3
    seg = int(segf)                    # 0,1,2
    t_f = segf - seg                   # 0..1 within segment

    # 2) integer t 0..255 for lerp
    t = int(t_f * 255.0 + 0.5)         # 0..255

    # 3) pick colors and crossfade
    a = PALETTE[seg]
    b = PALETTE[(seg + 1) % 3]
    r = (a[0] * (255 - t) + b[0] * t) >> 8
    g = (a[1] * (255 - t) + b[1] * t) >> 8
    bl = (a[2] * (255 - t) + b[2] * t) >> 8

    # 4) brightness curve: 75% at ends, 33% at midpoint
    # f = 4*t*(255-t)/255  (peaks at t≈127); we use (255 - f) so ends are brightest
    f_scaled = (4 * t * (255 - t)) // 255        # 0..255
    bri = MED_BRI_MIN + (MED_BRI_RANGE * (255 - f_scaled)) // 255  # 85..191

    # 5) scale + gamma, fill all pixels
    col = gamma_rgb(scale_rgb((r, g, bl), bri))
    for i in range(PIXEL_COUNT):
        pixels[i] = col


# ----------------------------
# Radial Fire (ring + center) — every pixel can spark
# ----------------------------
# Assumes 6 LEDs around and 1 in the center (total 7).
# If your center index is not 6, change CENTER_INDEX accordingly.
CENTER_INDEX = 6
assert PIXEL_COUNT == 7, "This radial model is tuned for 7 LEDs (6 ring + 1 center)."

# Tunables
COOLING = 6              # per-frame cooling (bigger = more flicker)
SPARK_CHANCE_RING = 20    # 0..255 chance a ring pixel sparks each frame
SPARK_CHANCE_CENTER = 20  # 0..255 chance center sparks each frame
SPARK_HEAT_RING = (20, 50)
SPARK_HEAT_CENTER = (60, 120)
EMAA = 64                 # temporal smoothing alpha (lower = smoother)
HOT_THRESHOLD = 200      # above this, apply extra cooling

# Diffusion weights: how much heat a pixel pulls from itself vs neighbors
W_SELF_RING   = 4
W_SIDE_RING   = 3  # each side neighbor (left/right on ring)
W_CENTER_TO_RING = 2

W_SELF_CENTER = 6
W_RING_TO_CENTER = 2  # each of the six ring neighbors

# Build adjacency for the 6-around-1 geometry
RING_IDXS = [i for i in range(PIXEL_COUNT) if i != CENTER_INDEX]

# neighbors map: for each pixel, list of (neighbor_index, weight)
NEIGHBORS = {i: [] for i in range(PIXEL_COUNT)}

# Ring pixels: neighbors are left, right, and center
for i in RING_IDXS:
    left  = RING_IDXS[(RING_IDXS.index(i) - 1) % len(RING_IDXS)]
    right = RING_IDXS[(RING_IDXS.index(i) + 1) % len(RING_IDXS)]
    NEIGHBORS[i].append((i, W_SELF_RING))
    NEIGHBORS[i].append((left, W_SIDE_RING))
    NEIGHBORS[i].append((right, W_SIDE_RING))
    NEIGHBORS[i].append((CENTER_INDEX, W_CENTER_TO_RING))

# Center pixel: neighbors are all ring pixels
NEIGHBORS[CENTER_INDEX].append((CENTER_INDEX, W_SELF_CENTER))
for i in RING_IDXS:
    NEIGHBORS[CENTER_INDEX].append((i, W_RING_TO_CENTER))

# Heat + smoothed RGB buffers
heat = [0] * PIXEL_COUNT            # 0..255
fire_rgb_smooth = [(0, 0, 0)] * PIXEL_COUNT
FIRE_SPEED = .9

def heat_to_color(h):
    """
    Map heat (0..255) to black-body-ish RGB (red/orange/yellow-white).
    """
    t192 = (h * 191) >> 8  # 0..191
    if t192 <= 63:
        r = t192 << 2; g = 0; b = 0
    elif t192 <= 127:
        j = t192 - 64
        r = 255; g = j << 2; b = 0
    else:
        j = t192 - 128
        r = 255; g = 255; b = j << 2
    if r > 255: r = 255
    if g > 255: g = 255
    if b > 255: b = 255
    return (r, g, b)
    
def fire_step(dt):
    global heat, fire_rgb_smooth

    # --- 1) cooling ---
    base_cool = int(COOLING * dt * 60 * FIRE_SPEED)
    if base_cool < 1:
        base_cool = 1

    for i in range(PIXEL_COUNT):
        # if a pixel is too hot, double the cooling
        cool = base_cool
        if heat[i] > HOT_THRESHOLD:
            cool *= 2

        val = heat[i] - random.randint(0, cool)
        if val < 0:
            val = 0
        heat[i] = val

    # --- 2) diffusion ---
    new_heat = [0] * PIXEL_COUNT
    for i in range(PIXEL_COUNT):
        num = 0
        den = 0
        for j, w in NEIGHBORS[i]:
            num += heat[j] * w
            den += w
        new_heat[i] = num // den if den else heat[i]
    heat[:] = new_heat

    # --- 3) sparks ---
    for i in RING_IDXS:
        if random.randint(0, 255) < int(SPARK_CHANCE_RING * dt * 60 * FIRE_SPEED):
            added = random.randint(SPARK_HEAT_RING[0], SPARK_HEAT_RING[1])
            h = heat[i] + added
            heat[i] = 255 if h > 255 else h
    if random.randint(0, 255) < int(SPARK_CHANCE_CENTER * dt * 60 * FIRE_SPEED):
        added = random.randint(SPARK_HEAT_CENTER[0], SPARK_HEAT_CENTER[1])
        h = heat[CENTER_INDEX] + added
        heat[CENTER_INDEX] = 255 if h > 255 else h

    # --- 4) heat -> color, 5) EMA + gamma ---
    for i in range(PIXEL_COUNT):
        tr, tg, tb = heat_to_color(heat[i])
        sr, sg, sb = fire_rgb_smooth[i]
        sr += ((tr - sr) * EMAA) >> 8
        sg += ((tg - sg) * EMAA) >> 8
        sb += ((tb - sb) * EMAA) >> 8
        fire_rgb_smooth[i] = (sr, sg, sb)
        pixels[i] = (GAMMA[sr], GAMMA[sg], GAMMA[sb])

# ---- Comet (sub-pixel head + gaussian falloff + EMA) ----
# Tunables
COMET_SPEED = 2.0        # LEDs per second (try 1.0–3.0)
COMET_COLOR = (180, 0, 255)
COMET_SIGMA = 0.55       # width of the head glow (gaussian; smaller = tighter, bigger = wider)
COMET_CUTOFF = 3.0       # don't bother computing beyond this distance
COMET_EMA = 96           # 0..255 temporal smoothing (96≈0.38). Lower = smoother/lingers longer.

# State
comet_pos = 0.0
comet_dir = 1
# keep a smoothed RGB buffer so the comet fades between frames
try:
    comet_rgb_smooth
except NameError:
    comet_rgb_smooth = [(0, 0, 0)] * PIXEL_COUNT

def _gauss(dist):
    # exp(-(d^2)/(2*sigma^2))
    # For very small arrays this math cost is fine; if you want, precompute a tiny LUT.
    return math.exp(-(dist * dist) / (2.0 * COMET_SIGMA * COMET_SIGMA))

def comet_step(dt):
    global comet_pos, comet_dir, comet_rgb_smooth

    # 1) advance with sub-pixel precision
    comet_pos += dt * COMET_SPEED * comet_dir

    # 2) bounce with overshoot reflection (prevents "sticking" on ends)
    max_i = PIXEL_COUNT - 1
    if comet_pos > max_i:
        overshoot = comet_pos - max_i
        comet_pos = max_i - overshoot
        comet_dir = -1
    elif comet_pos < 0.0:
        overshoot = 0.0 - comet_pos
        comet_pos = 0.0 + overshoot
        comet_dir = 1

    # 3) render: gaussian falloff around head -> target RGBs
    #    LEDs far from head get 0; nearby LEDs blend smoothly as the head crosses.
    trgb = [ (0,0,0) ] * PIXEL_COUNT
    br, bg, bb = COMET_COLOR
    for i in range(PIXEL_COUNT):
        d = abs(i - comet_pos)
        if d > COMET_CUTOFF:
            continue
        # brightness 0..255
        bri = int(255.0 * _gauss(d))
        if bri <= 0:
            continue
        tr = (br * bri) // 255
        tg = (bg * bri) // 255
        tb = (bb * bri) // 255
        trgb[i] = (tr, tg, tb)

    # 4) temporal EMA smoothing for lingering/fade (prevents popping when head crosses LED centers)
    #    smooth += alpha*(target - smooth) / 256
    a = COMET_EMA
    for i in range(PIXEL_COUNT):
        sr, sg, sb = comet_rgb_smooth[i]
        tr, tg, tb = trgb[i]
        sr += ((tr - sr) * a) >> 8
        sg += ((tg - sg) * a) >> 8
        sb += ((tb - sb) * a) >> 8
        comet_rgb_smooth[i] = (sr, sg, sb)
        pixels[i] = gamma_rgb((sr, sg, sb))  # keep your existing gamma


# 5) Chase (moving block)
chase_pos = 0
chase_accum = 0.0
CHASE_SPEED = 10.0  # LEDs per second
CHASE_SIZE = 3
CHASE_SPACING = 1
CHASE_COLOR = (255, 255, 255)

def chase_step(dt):
    global chase_pos, chase_accum
    chase_accum += dt * CHASE_SPEED
    moved = int(chase_accum)
    if moved:
        chase_accum -= moved
        chase_pos = (chase_pos + moved) % (PIXEL_COUNT + CHASE_SPACING)

    # Clear
    for i in range(PIXEL_COUNT):
        pixels[i] = (0, 0, 0)

    # Draw a "block" of CHASE_SIZE starting at chase_pos
    col = gamma_rgb(CHASE_COLOR)
    for k in range(CHASE_SIZE):
        idx = (chase_pos + k) % PIXEL_COUNT
        pixels[idx] = col

# ----------------------------
# Fixed fills (modes 4..8)
# ----------------------------
FILL_COLORS = {
    4: (60, 60, 60),
    5: (100, 100, 100),
    6: (160, 160, 160),
    7: (240, 240, 240),
    8: (0, 0, 0),
}

# ----------------------------
# Main animation dispatcher
# ----------------------------
def run_current_animation(dt):
    if animationMode == 0:
        fire_step(dt)
    elif animationMode == 1:
        rainbow_step()
    elif animationMode == 2:
        comet_step(dt)
    elif animationMode == 3:
        meditation_step(dt)
    elif animationMode in FILL_COLORS:
        fill_const(FILL_COLORS[animationMode])
    elif animationMode == 9:
        chase_step(dt)

# ----------------------------
# Main loop
# ----------------------------
# Ensure a known initial state
fill_const((0, 0, 0))
pixels.show()

while True:
    now = time.monotonic()
    if now >= next_frame:
        # Compute dt relative to intended frame cadence; keep it bounded
        dt = now - next_frame + FRAME
        if dt < 0:
            dt = FRAME
        elif dt > 0.25:
            dt = 0.25  # avoid big jumps if system stalls

        next_frame += FRAME

        update_button()
        run_current_animation(dt)

        pixels.show()
    else:
        # precise sleep until next frame
        time.sleep(next_frame - now)
