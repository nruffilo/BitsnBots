import audiocore
import board
import audiobusio
from digitalio import DigitalInOut, Direction, Pull

btn = DigitalInOut(board.GP17)

wave_file = open("harrypotter.wav", "rb")
wave = audiocore.WaveFile(wave_file)

audio = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)

while True:
    print("Playing sound...")
    print(btn.value)
    #audio.play(wave)
    #while audio.playing:
    #    pass
