"""One-time script: generates placeholder sound/sprite assets into assets/.
Run once with `uv run make_assets.py` -- not part of the game itself.
"""

import math
import os
import struct
import wave

import pygame

os.makedirs("assets", exist_ok=True)


def write_tone(filename, freq_start, freq_end, duration, volume=0.5):
    framerate = 44100
    n_frames = int(framerate * duration)
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(framerate)
        for i in range(n_frames):
            t = i / framerate
            freq = freq_start + (freq_end - freq_start) * (i / n_frames)
            sample = volume * math.sin(2 * math.pi * freq * t)
            fade = 1 - (i / n_frames)  # avoids a clicking sound at the end
            packed = struct.pack("<h", int(sample * fade * 32767))
            wav_file.writeframesraw(packed)


write_tone("assets/flap.wav", freq_start=400, freq_end=800, duration=0.12)
write_tone("assets/hit.wav", freq_start=300, freq_end=100, duration=0.25)

pygame.init()
bird_surface = pygame.Surface((50, 40), pygame.SRCALPHA)
pygame.draw.circle(bird_surface, (255, 255, 0), (20, 20), 18)  # body
pygame.draw.circle(bird_surface, (0, 0, 0), (26, 14), 3)  # eye
pygame.draw.polygon(bird_surface, (255, 140, 0), [(36, 20), (48, 15), (48, 25)])  # beak
pygame.image.save(bird_surface, "assets/bird.png")

print("Wrote assets/flap.wav, assets/hit.wav, assets/bird.png")
