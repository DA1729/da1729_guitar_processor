import numpy as np
from scipy import signal as sp_signal


def biquad(input_signal, b0, b1, b2, a1, a2):
    output_signal = np.zeros_like(input_signal)

    x_1 = 0.0
    x_2 = 0.0
    y_1 = 0.0
    y_2 = 0.0

    for i in range(len(input_signal)):
        x_0 = input_signal[i]

        y_0 = (b0 * x_0) + (b1 * x_1) + (b2 * x_2) - (a1 * y_1) - (a2 * y_2)

        x_2 = x_1
        x_1 = x_0
        y_2 = y_1
        y_1 = y_0

        output_signal[i] = y_0

    return output_signal


def lowpass(signal, fs, cutoff_freq=800.0, order=2):
    sos = sp_signal.butter(N=order, Wn=cutoff_freq, btype='low', fs=fs, output='sos')
    coeffs = sos[0]
    b0, b1, b2, a0, a1, a2 = coeffs

    return biquad(signal, b0, b1, b2, a1, a2)


def highpass(signal, fs, cutoff_freq=800.0, order=2):
    sos = sp_signal.butter(N=order, Wn=cutoff_freq, btype='high', fs=fs, output='sos')
    coeffs = sos[0]
    b0, b1, b2, a0, a1, a2 = coeffs

    return biquad(signal, b0, b1, b2, a1, a2)


def bandpass(signal, fs, low_freq=300.0, high_freq=3000.0, order=2):
    sos = sp_signal.butter(N=order, Wn=[low_freq, high_freq], btype='band', fs=fs, output='sos')
    coeffs = sos[0]
    b0, b1, b2, a0, a1, a2 = coeffs

    return biquad(signal, b0, b1, b2, a1, a2)
