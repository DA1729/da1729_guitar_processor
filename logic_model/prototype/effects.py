import numpy as np


def hard_clip(signal, gain=10.0, threshold=0.5):
    boosted = signal * gain
    clipped = np.clip(boosted, -threshold, threshold)
    return clipped / threshold


def soft_clip(signal, gain=10.0):
    boosted = signal * gain
    return np.tanh(boosted)
