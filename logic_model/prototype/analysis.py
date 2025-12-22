import numpy as np
import matplotlib.pyplot as plt


def plot_time_domain(signals_dict, fs, window_ms=50, save_path=None):
    fig, ax = plt.subplots(figsize=(12, 6))

    first_signal = list(signals_dict.values())[0]
    peak_idx = np.argmax(np.abs(first_signal))

    window_samples = int(fs * (window_ms / 1000))
    start_idx = max(0, peak_idx - window_samples // 2)
    end_idx = min(len(first_signal), start_idx + window_samples)

    t_axis = np.linspace(0, window_ms, end_idx - start_idx)

    for label, signal in signals_dict.items():
        ax.plot(t_axis, signal[start_idx:end_idx], label=label, alpha=0.7)

    ax.set_xlabel('time (ms)')
    ax.set_ylabel('amplitude')
    ax.set_title('time domain')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    return fig


def plot_frequency_domain(signals_dict, fs, fft_size=4096, freq_limit=3000, save_path=None):
    fig, ax = plt.subplots(figsize=(12, 6))

    for label, signal in signals_dict.items():
        fft_slice = signal[:min(len(signal), fft_size)]
        spectrum = np.fft.fft(fft_slice, n=fft_size)
        freqs = np.fft.fftfreq(fft_size, 1/fs)
        magnitude = np.abs(spectrum)

        idx_limit = int(freq_limit * fft_size / fs)
        ax.plot(freqs[:idx_limit], magnitude[:idx_limit], label=label, alpha=0.7)

    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel('magnitude')
    ax.set_title('frequency domain')
    ax.set_xlim(0, freq_limit)
    ax.legend()
    ax.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    return fig


def plot_comparison(signals_dict, fs, window_ms=50, fft_size=4096, freq_limit=3000, save_path=None):
    fig = plt.figure(figsize=(12, 10))

    first_signal = list(signals_dict.values())[0]
    peak_idx = np.argmax(np.abs(first_signal))

    window_samples = int(fs * (window_ms / 1000))
    start_idx = max(0, peak_idx - window_samples // 2)
    end_idx = min(len(first_signal), start_idx + window_samples)

    t_axis = np.linspace(0, window_ms, end_idx - start_idx)

    ax1 = plt.subplot(2, 1, 1)
    for label, signal in signals_dict.items():
        ax1.plot(t_axis, signal[start_idx:end_idx], label=label, alpha=0.7)

    ax1.set_xlabel('time (ms)')
    ax1.set_ylabel('amplitude')
    ax1.set_title('time domain')
    ax1.legend()
    ax1.grid(True)

    ax2 = plt.subplot(2, 1, 2)
    for label, signal in signals_dict.items():
        fft_slice = signal[start_idx:start_idx + min(fft_size, len(signal) - start_idx)]
        spectrum = np.fft.fft(fft_slice, n=fft_size)
        freqs = np.fft.fftfreq(fft_size, 1/fs)
        magnitude = np.abs(spectrum)

        idx_limit = int(freq_limit * fft_size / fs)
        ax2.plot(freqs[:idx_limit], magnitude[:idx_limit], label=label, alpha=0.7)

    ax2.set_xlabel('frequency (Hz)')
    ax2.set_ylabel('magnitude')
    ax2.set_title('frequency domain')
    ax2.set_xlim(0, freq_limit)
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    return fig
