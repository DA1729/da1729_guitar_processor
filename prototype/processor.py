import numpy as np


class guitar_processor:
    def __init__(self, fs, signal):
        self.fs = fs
        self.signal = signal
        self.processed = signal.copy()
        self.history = {'input': signal.copy()}

    def apply(self, effect_fn, name=None, **kwargs):
        self.processed = effect_fn(self.processed, **kwargs)

        if name:
            self.history[name] = self.processed.copy()

        return self

    def get_signal(self):
        return self.processed

    def get_history(self):
        return self.history

    def reset(self):
        self.processed = self.signal.copy()
        self.history = {'input': self.signal.copy()}
        return self
