import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def load_and_normalize(filename):
    fs, data = wavfile.read(filename)

    if data.dtype == np.int16:
        data = data/32768.0

    if len(data.shape) > 1:
        data = data[:, 0]


    return fs, data

def save_wav(filename, signal, fs):
    scaled = np.int16(signal * 32767)
    wavfile.write(filename, fs, scaled)
    print(f"Saved: {filename}")


fs, clean_signal = load_and_normalize('dry_guitar.wav')

print(f"sample rate: {fs}Hz, total samples: {len(clean_signal)}")


def compute_envelope(signal, fs, attack_ms, release_ms):
    num_samples = len(signal)
    envelop = np.zeros(num_samples)

    attack_coeff = np.exp(-1000.0/(fs * attack_ms))
    release_coeff = np.exp(-1000.0/(fs * release_ms))

    current_level = 0.0

    for i in range(num_samples):
        abs_input = abs(signal[i])

        if abs_input > current_level:
            # attack phase
            current_level = (attack_coeff * current_level) + ((1 - attack_coeff) * abs_input)   
        else:
            current_level = (release_coeff * current_level) + ((1 - release_coeff) * abs_input)

        envelop[i] = current_level

    return envelop


def noise_gate(signal, fs, threshold_db = -40.0, attack_ms = 2.0, release_ms = 100.0, hold_ms = 10.0):

    env = compute_envelope(signal, fs, attack_ms, release_ms)

    env_db = 20 * np.log10(env + 1e-6)

    gain_curve = np.ones_like(signal)

    target_gain = np.where(env_db < threshold_db, 0.0, 1.0)

    smooth_gain = compute_envelope(target_gain, fs, attack_ms, release_ms)

    return signal * smooth_gain, smooth_gain

def compressor(signal, fs, threshold_db = -20.0, ratio = 4.0, attack_ms = 5.0, release_ms = 50.0, makeup_gain_db = 5.0):

    env = compute_envelope(signal, fs, attack_ms, release_ms)
    env_db = 20 * np.log10(env + 1e-6)

    over_db = env_db - threshold_db
    over_db = np.maximum(over_db, 0)

    gain_reduction_db = over_db * (1 - (1/ratio))

    gain_linear = np.power(10, -gain_reduction_db / 20.0)

    makeup_linear = np.power(10, makeup_gain_db / 20.0)

    return signal * gain_linear * makeup_linear, gain_linear

fs = 44100
t = np.linspace(0, 4, 4 * fs)
sig_quiet = 0.1 * np.sin(2*np.pi*440*t) * ((t > 0.5) & (t < 1.5))
sig_loud = 0.8 * np.sin(2*np.pi*440*t) * ((t > 2.0) & (t < 3.0))
noise = 0.005 * np.random.normal(0, 1, len(t))

raw_signal = sig_quiet + sig_loud + noise

gate_out, gate_gain = noise_gate(raw_signal, fs, threshold_db=-30.0)
comp_out, comp_gain = compressor(raw_signal, fs, threshold_db=-20.0, ratio=4.0, makeup_gain_db=6.0)

plt.figure(figsize=(12, 10))

plt.subplot(3, 1, 1)
plt.plot(t, raw_signal, label='Input (with noise)', color='gray', alpha=0.5)
plt.plot(t, gate_out, label='Gated Output', color='green', alpha=0.8)
plt.axhline(0.005, color='red', linestyle=':', label='Approx Noise Floor')
plt.title('Noise Gate')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, raw_signal, label='Input', color='gray', alpha=0.5)
plt.plot(t, comp_out, label='Compressed', color='blue', alpha=0.8)
plt.axhline(0.1, color='orange', linestyle='--', label='Threshold')
plt.title('Compressor')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t, gate_gain, label='Gate Gain (1.0 = Open, 0.0 = Closed)', color='green')
plt.plot(t, comp_gain, label='Compressor Gain Reduction', color='blue')
plt.title('Internal Gain Control Signals')
plt.xlabel('Time (s)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('./plots/dynamics.png')
