import sys
sys.path.insert(0, '/home/vincent/Projects/guitar_processor')

import numpy as np
from prototype import (
    load_audio,
    save_audio,
    fuzz,
    overdrive,
    cabinet,
    lowpass,
    highpass,
    guitar_processor
)


fs, clean_signal = load_audio('/home/vincent/Projects/guitar_processor/logic_model/dry_guitar.wav')

proc = guitar_processor(fs, clean_signal)

proc.apply(highpass, 'hp_cleanup', fs=fs, cutoff_freq=80.0, order=2)
proc.apply(fuzz, 'fuzz', gain=15.0, threshold=0.4)
proc.apply(lowpass, 'tone', fs=fs, cutoff_freq=5000.0, order=2)
proc.apply(cabinet, 'cab', fs=fs, duration_ms=20)

processed = proc.get_signal()

save_audio('/home/vincent/Projects/guitar_processor/logic_model/output_wav/chained_output.wav', processed, fs, verbose=True)

print(f"processed {len(clean_signal)} samples at {fs}Hz")
print(f"chain: {' -> '.join(proc.get_history().keys())}")
