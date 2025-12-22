import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

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

cutoff_freq = 800 #Hz
sos = signal.butter(N = 2, Wn = cutoff_freq, btype = 'low', fs = fs, output = 'sos')
coeffs = sos[0]
b0, b1, b2, a0, a1, a2 = coeffs

print('filter coefficients: ')
print(f'b0: {b0:.4f}, b1: {b1:.4f}, b2: {b2:.4f}')
print(f'a1: {a1:.4f}, a2: {a2:.4f}')


def apply_biquad(input_signal, b0, b1, b2, a1, a2):
    output_signal = np.zeros_like(input_signal)

    x_1 = 0.0 # x[n-1]
    x_2 = 0.0 # x[n-2]
    y_1 = 0.0 # y[n-1]
    y_2 = 0.0 # y[n-2]

    print('processing filter...')

    for i in range(len(input_signal)):
        x_0 = input_signal[i]

        y_0 = (b0 * x_0) + (b1 * x_1) + (b2 * x_2) - (a1 * y_1) - (a2 * y_2)

        x_2 = x_1
        x_1 = x_0
        y_2 = y_1
        y_1 = y_0

        output_signal[i] = y_0

    return output_signal


filtered_signal = apply_biquad(clean_signal, b0, b1, b2, a1, a2)


wavfile.write('./output_wav/filtered.wav', fs, np.int16(filtered_signal * 32767))

plt.figure(figsize=(10, 8))



chunk_size = 4096
clean_fft = np.abs(np.fft.fft(clean_signal[:chunk_size]))
filt_fft = np.abs(np.fft.fft(filtered_signal[:chunk_size]))
freqs = np.fft.fftfreq(chunk_size, 1/fs)

plt.subplot(2,1,1)
limit = 5000 # 5kHz limit
idx = int(limit * chunk_size / fs)

plt.plot(freqs[:idx], clean_fft[:idx], label='Original', color='gray', alpha=0.5)
plt.plot(freqs[:idx], filt_fft[:idx], label='Filtered (Low Pass @ 800Hz)', color='red')
plt.title('Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('./plots/filter.png')

