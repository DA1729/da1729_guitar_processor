import numpy as np


def compute_envelope(signal, fs, attack_ms, release_ms):
    num_samples = len(signal)
    envelope = np.zeros(num_samples)

    attack_coeff = np.exp(-1000.0 / (fs * attack_ms))
    release_coeff = np.exp(-1000.0 / (fs * release_ms))

    current_level = 0.0

    for i in range(num_samples):
        abs_input = abs(signal[i])

        if abs_input > current_level:
            current_level = (attack_coeff * current_level) + ((1 - attack_coeff) * abs_input)
        else:
            current_level = (release_coeff * current_level) + ((1 - release_coeff) * abs_input)

        envelope[i] = current_level

    return envelope


def noise_gate(signal, fs, threshold_db=-40.0, attack_ms=2.0, release_ms=100.0, hold_ms=10.0):
    env = compute_envelope(signal, fs, attack_ms, release_ms)
    env_db = 20 * np.log10(env + 1e-6)

    target_gain = np.where(env_db < threshold_db, 0.0, 1.0)
    smooth_gain = compute_envelope(target_gain, fs, attack_ms, release_ms)

    return signal * smooth_gain


def compressor(signal, fs, threshold_db=-20.0, ratio=4.0, attack_ms=5.0, release_ms=50.0, makeup_gain_db=5.0):
    env = compute_envelope(signal, fs, attack_ms, release_ms)
    env_db = 20 * np.log10(env + 1e-6)

    over_db = env_db - threshold_db
    over_db = np.maximum(over_db, 0)

    gain_reduction_db = over_db * (1 - (1 / ratio))

    gain_linear = np.power(10, -gain_reduction_db / 20.0)
    makeup_linear = np.power(10, makeup_gain_db / 20.0)

    return signal * gain_linear * makeup_linear
