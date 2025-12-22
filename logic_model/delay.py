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


def apply_delay(input_signal, fs, delay_ms, feedback, mix):
    delay_samples = int(fs * (delay_ms/1000.0))
    total_len = len(input_signal) + delay_samples * 5 # roughly 5 repeats
    #output_signal = np.zeros(total_len)

    padded_input = np.zeros(total_len)
    padded_input[:len(input_signal)] = input_signal

    wet_buffer = np.zeros(total_len)

    print("processing delay...")

    for i in range(total_len):
        dry_sample = padded_input[i]

        if i >= delay_samples:
            delayed_sample = wet_buffer[i - delay_samples]
        else:
            delayed_sample = 0.0
        
        wet_sample = delayed_sample * feedback      # scaled up delayed sample

        wet_buffer[i] = dry_sample + wet_sample

    dry_gain = 1.0 - mix
    wet_gain = mix
    
    wet_slice = wet_buffer[:len(input_signal)]

    final_output = (input_signal * dry_gain) + (wet_slice * wet_gain)

    return final_output

delay_signal = apply_delay(clean_signal, fs, delay_ms=400, feedback=0.6, mix=0.5)
print('processing finished')

wavfile.write('./output_wav/delay_echo.wav', fs, np.int16(delay_signal * 32767))
print("Saved: delay_echo.wav")


plt.figure(figsize=(12, 6))

peak = np.argmax(np.abs(clean_signal))
start = peak
duration_samples = int(1.5 * fs)
end = min(len(clean_signal), start + duration_samples)
t = np.linspace(0, 1.5, end-start)

plt.plot(t, clean_signal[start:end], label='Dry Input', alpha=0.5, color='gray')
plt.plot(t, delay_signal[start:end], label='Wet Output (With Echoes)', alpha=0.8, color='blue')

plt.title('Time Domain')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./plots/delay.png')
