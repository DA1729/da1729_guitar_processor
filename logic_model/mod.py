import numpy as np
import matplotlib.pyplot as plt

class LFO:

    def __init__(self, fs, rate_hz, waveform = 'sine'):
        self.fs = fs
        self.rate = rate_hz
        self.phase = 0.0
        self.waveform = waveform

    # to be completed

