
import simpleaudio as sa
from pathlib import Path

class SoundPlayer:
    def __init__(self, wav_path: str):
        self.wav_path = Path(wav_path)

    def play(self):
        if not self.wav_path.exists():
            print(f"[SoundPlayer] Missing sound file: {self.wav_path}")
            return False
        try:
            wave_obj = sa.WaveObject.from_wave_file(str(self.wav_path))
            wave_obj.play()  # non-blocking
            print("[SoundPlayer] Played deterrent sound.")
            return True
        except Exception as e:
            print(f"[SoundPlayer] Error: {e}")
            return False
