import numpy as np
from scipy import signal as sp_signal


def fuzz(signal, gain=10.0, threshold=0.5):
    boosted = signal * gain
    clipped = np.clip(boosted, -threshold, threshold)
    return clipped / threshold


def overdrive(signal, gain=10.0):
    boosted = signal * gain
    return np.tanh(boosted)


def delay(signal, fs, delay_ms=400.0, feedback=0.6, mix=0.5):
    delay_samples = int(fs * (delay_ms / 1000.0))
    total_len = len(signal) + delay_samples * 5

    padded_input = np.zeros(total_len)
    padded_input[:len(signal)] = signal

    wet_buffer = np.zeros(total_len)

    for i in range(total_len):
        dry_sample = padded_input[i]

        if i >= delay_samples:
            delayed_sample = wet_buffer[i - delay_samples]
        else:
            delayed_sample = 0.0

        wet_sample = delayed_sample * feedback
        wet_buffer[i] = dry_sample + wet_sample

    dry_gain = 1.0 - mix
    wet_gain = mix

    wet_slice = wet_buffer[:len(signal)]
    output = (signal * dry_gain) + (wet_slice * wet_gain)

    return output


def generate_cab_ir(fs, duration_ms=20):
    N = int(fs * (duration_ms / 1000.0))
    t = np.linspace(0, duration_ms / 1000.0, N)

    resonance = np.sin(2 * np.pi * 100 * t) * np.exp(-t * 300)

    fc = 4000
    w = 2 * np.pi * fc / fs
    low_pass = np.sinc(w * (np.arange(N) - N / 2))

    ir = resonance + low_pass
    ir = ir * np.hanning(N)

    return ir / np.max(np.abs(ir))


def cabinet(signal, fs, ir=None, duration_ms=20):
    if ir is None:
        ir = generate_cab_ir(fs, duration_ms)

    output = sp_signal.convolve(signal, ir, mode='same')
    return output / np.max(np.abs(output))
