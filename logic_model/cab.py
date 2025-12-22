import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# --- 1. Load Data ---
def load_and_normalize(filename):
    fs, data = wavfile.read(filename)
    if data.dtype == np.int16:
        data = data / 32768.0
    if len(data.shape) > 1:
        data = data[:, 0]
    return fs, data

fs, clean_signal = load_and_normalize('dry_guitar.wav')

print(f"sample rate: {fs}Hz, total samples: {len(clean_signal)}")

# mathematically modelling a cab's respone, irl download .wav file of some famous cab
def generate_cab_ir(fs, duration_ms = 20):
    N = int(fs * (duration_ms/1000.0))
    ir = np.zeros(N)

    t = np.linspace(0, duration_ms/1000.0, N)
    resonance = np.sin(2 * np.pi * 100 * t) * np.exp(-t * 300) # decays quickly

    # LPF using the sinc function
    fc = 4000 # cutoff at 4kHz
    w = 2 * np.pi * fc / fs
    low_pass = np.sinc(w * (np.arange(N) - N/2))

    ir = resonance + low_pass

    ir = ir * np.hanning(N)
    
    return ir / np.max(np.abs(ir)) # normalize


print('generating synthetic cabinet IR...')
cabinet_ir = generate_cab_ir(fs)
wavfile.write('./output_wav/cabinet_ir.wav', fs, np.int16(cabinet_ir * 32767))

print('convolving (applying the cab)...')

cab_signal = signal.convolve(clean_signal, cabinet_ir, mode='same')

cab_signal = cab_signal / np.max(np.abs(cab_signal))
wavfile.write('./output_wav/cabinet_sim.wav', fs, np.int16(cab_signal * 32767))


plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(cabinet_ir)
plt.title('The Synthetic Impulse Response (Time Domain)')
plt.grid(True)

chunk = 4096
clean_fft = np.abs(np.fft.fft(clean_signal[:chunk]))
cab_fft = np.abs(np.fft.fft(cab_signal[:chunk]))
freqs = np.fft.fftfreq(chunk, 1/fs)

plt.subplot(2, 1, 2)
limit = 1000
idx = int(limit * chunk / fs)

plt.plot(freqs[:idx], clean_fft[:idx], label='Raw DI (Harsh)', alpha=0.5)
plt.plot(freqs[:idx], cab_fft[:idx], label='Cabinet Sim (Smoothed)', color='red')
plt.title('Effect of Cabinet on Frequency')
plt.xlabel('Frequency (Hz)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('./plots/cab.png')

