import numpy as np
from scipy.io import wavfile


def load_audio(filename):
    fs, data = wavfile.read(filename)
    return fs, normalize_audio(data)


def normalize_audio(data):
    if data.dtype == np.int16:
        data = data / 32768.0
    elif data.dtype == np.int32:
        data = data / 2147483648.0

    if len(data.shape) > 1:
        data = data[:, 0]

    return data


def save_audio(filename, signal, fs, verbose=False):
    signal_clipped = np.clip(signal, -1.0, 1.0)
    scaled = np.int16(signal_clipped * 32767)
    wavfile.write(filename, fs, scaled)

    if verbose:
        print(f"saved: {filename}")
