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
    

fs, audio_in = load_and_normalize('dry_guitar.wav')

print(f"sample rate: {fs}Hz, total samples: {len(audio_in)}")

peak_index = np.argmax(np.abs(audio_in))

window_size_ms = 50
window_samples = int(fs * (window_size_ms / 1000))

start_idx = max(0, peak_index - window_samples // 2)
end_idx = min(len(audio_in), start_idx + window_samples)

time_slice = audio_in[start_idx:end_idx]
t_axis = np.linspace(0, window_size_ms, len(time_slice))

plt.figure(figsize=(12, 8))


plt.subplot(2, 1, 1)
plt.plot(t_axis, time_slice)
plt.title(f'time domain')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (normalized)')
plt.grid(True)

fft_size = 4096

if len(audio_in) < fft_size:
    fft_size = len(audio_in)

fft_slice = audio_in[start_idx : start_idx + fft_size]
spectrum = np.fft.fft(fft_slice)
freqs = np.fft.fftfreq(len(fft_slice), 1/fs)
magnitude = np.abs(spectrum)

plt.subplot(2, 1, 2)

plt.plot(freqs[:fft_size//2], magnitude[:fft_size//2])
plt.xlim(0, 2000)
plt.title('frequency domain')
plt.xlabel('frequency (Hz)')
plt.ylabel('magnitude')
plt.grid(True)

plt.tight_layout()
plt.savefig("time-freq-domain.png")

