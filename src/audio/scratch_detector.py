
import numpy as np
import sounddevice as sd
from dataclasses import dataclass

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    block_s: float = 0.5
    highband_hz: int = 4000
    energy_ratio: float = 2.5
    min_blocks: int = 3

class ScratchDetector:
    def __init__(self, cfg: AudioConfig):
        self.cfg = cfg
        self._confirmed = 0

    def _band_energy_ratio(self, audio):
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        n = len(audio)
        if n == 0:
            return 0.0
        window = np.hanning(n)
        spec = np.fft.rfft(audio * window)
        mag = np.abs(spec)
        freqs = np.fft.rfftfreq(n, d=1.0 / self.cfg.sample_rate)
        high = mag[freqs >= self.cfg.highband_hz].mean() + 1e-9
        low = mag[freqs < self.cfg.highband_hz].mean() + 1e-9
        return float(high / low)

    def stream_generator(self):
        blocksize = int(self.cfg.sample_rate * self.cfg.block_s)
        with sd.InputStream(samplerate=self.cfg.sample_rate, channels=1, blocksize=blocksize) as stream:
            while True:
                audio, _ = stream.read(blocksize)
                yield audio.squeeze()

    def is_scratching(self, audio_block):
        ratio = self._band_energy_ratio(audio_block)
        if ratio >= self.cfg.energy_ratio:
            self._confirmed += 1
        else:
            self._confirmed = max(0, self._confirmed - 1)
        return (self._confirmed >= self.cfg.min_blocks), ratio
