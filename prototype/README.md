# Guitar Processor Prototype

production-like structured codebase for guitar effects processing

## progress

- audio i/o with normalization
- distortion effects (fuzz, overdrive)
- delay/echo effect
- time/frequency domain analysis
- effect chaining via processor class

## structure

```
prototype/
├── audio_io.py     # load/save/normalize audio
├── effects.py      # guitar effects
├── analysis.py     # visualization tools
└── processor.py    # effect chain processor
```

## usage

### audio i/o

```python
from prototype import load_audio, save_audio

fs, signal = load_audio('input.wav')
save_audio('output.wav', processed_signal, fs, verbose=True)
```

**parameters:**
- `load_audio(filename)` → returns `(fs, signal)`
- `save_audio(filename, signal, fs, verbose=False)`
- `normalize_audio(data)` → returns normalized array

### effects

```python
from prototype import fuzz, overdrive, delay

fuzz_signal = fuzz(signal, gain=20.0, threshold=0.3)
overdrive_signal = overdrive(signal, gain=5.0)
echo = delay(signal, fs, delay_ms=400.0, feedback=0.6, mix=0.5)
```

**fuzz** - hard clipping distortion, adds harsh harmonics
- `gain` (default: 10.0) - pre-clip amplification, higher = more clipping
- `threshold` (default: 0.5) - clipping ceiling, lower = more aggressive

**overdrive** - smooth tanh saturation, warm distortion
- `gain` (default: 10.0) - drive amount, higher = more saturation

**delay** - tape-style echo with feedback
- `delay_ms` (default: 400.0) - time between echoes in milliseconds
- `feedback` (default: 0.6) - repeat strength [0.0-1.0], higher = more repeats
- `mix` (default: 0.5) - wet/dry blend [0.0-1.0], 0.0=dry only, 1.0=wet only

### analysis

```python
from prototype import plot_time_domain, plot_frequency_domain, plot_comparison

plot_comparison({'clean': signal, 'fuzz': fuzz}, fs, save_path='plot.png')
```

**parameters:**
- `plot_time_domain(signals_dict, fs, window_ms=50, save_path=None)`
- `plot_frequency_domain(signals_dict, fs, fft_size=4096, freq_limit=3000, save_path=None)`
- `plot_comparison(signals_dict, fs, window_ms=50, fft_size=4096, freq_limit=3000, save_path=None)`

### processor (effect chaining)

```python
from prototype import guitar_processor, fuzz, overdrive, delay

proc = guitar_processor(fs, signal)
proc.apply(fuzz, 'fuzz', gain=20.0, threshold=0.3)
proc.apply(overdrive, 'overdrive', gain=3.0)
proc.apply(delay, 'echo', fs=fs, delay_ms=300.0, feedback=0.5, mix=0.4)

result = proc.get_signal()
history = proc.get_history()  # dict of all processed stages
proc.reset()  # back to input signal
```

**parameters:**
- `guitar_processor(fs, signal)`
- `apply(effect_fn, name=None, **kwargs)` - chain effects, returns self
- `get_signal()` - returns current processed signal
- `get_history()` - returns dict of all named stages
- `reset()` - resets to input signal

## quick example

```python
from prototype import load_audio, save_audio, fuzz, plot_comparison

fs, signal = load_audio('dry_guitar.wav')
fuzz_signal = fuzz(signal, gain=20.0, threshold=0.3)
save_audio('fuzz_out.wav', fuzz_signal, fs)
plot_comparison({'input': signal, 'output': fuzz_signal}, fs, save_path='result.png')
```
