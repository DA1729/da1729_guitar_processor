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

# fuzz
def hard_clip(signal, gain = 10.0, threshold = 0.5):
    boosted = signal * gain
    output = np.clip(boosted, -threshold, threshold)
    return output / threshold

# overdrive
def soft_clip(signal, gain = 10.0):
    boosted = signal * gain
    output = np.tanh(boosted)
    return output

fuzz_signal = hard_clip(clean_signal, gain=20.0, threshold=0.3)
overdrive_signal = soft_clip(clean_signal, gain=5.0)

save_wav('fuzz.wav', fuzz_signal, fs)
save_wav('overdrive.wav', overdrive_signal, fs)

start = np.argmax(np.abs(clean_signal))
window = 200
end = start + window

t = np.arange(window)

plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(t, clean_signal[start:end], label='Clean', color='green', alpha=0.6)
plt.plot(t, fuzz_signal[start:end], label='Fuzz (Hard Clip)', color='red', linestyle='--')
plt.plot(t, overdrive_signal[start:end], label='Overdrive (Soft Clip)', color='blue')
plt.title('Time Domain')
plt.legend()
plt.grid(True)

fft_slice_len = 4096
clean_fft = np.abs(np.fft.fft(clean_signal[start:start+fft_slice_len]))
fuzz_fft = np.abs(np.fft.fft(fuzz_signal[start:start+fft_slice_len]))
freqs = np.fft.fftfreq(fft_slice_len, 1/fs)

plt.subplot(2, 1, 2)
limit = 3000
idx_limit = int(limit * fft_slice_len / fs)

plt.plot(freqs[:idx_limit], clean_fft[:idx_limit], label='Clean', color='green', alpha=0.5)
plt.plot(freqs[:idx_limit], fuzz_fft[:idx_limit], label='Fuzz (Added Harmonics)', color='red', alpha=0.5)

plt.title('Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("fuzz_od.png")
