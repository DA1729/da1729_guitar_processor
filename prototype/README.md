# Guitar Processor Prototype

production-like structured codebase for guitar effects processing

## progress

- audio i/o with normalization
- distortion effects (fuzz, overdrive)
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
from prototype import hard_clip, soft_clip

fuzz = hard_clip(signal, gain=20.0, threshold=0.3)
overdrive = soft_clip(signal, gain=5.0)
```

**parameters:**
- `hard_clip(signal, gain=10.0, threshold=0.5)` - fuzz/hard clipping
- `soft_clip(signal, gain=10.0)` - overdrive/tanh saturation

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
from prototype import AudioProcessor, hard_clip, soft_clip

proc = AudioProcessor(fs, signal)
proc.apply(hard_clip, 'fuzz', gain=20.0, threshold=0.3)
proc.apply(soft_clip, 'overdrive', gain=3.0)

result = proc.get_signal()
history = proc.get_history()  # dict of all processed stages
proc.reset()  # back to input signal
```

**parameters:**
- `AudioProcessor(fs, signal)`
- `apply(effect_fn, name=None, **kwargs)` - chain effects, returns self
- `get_signal()` - returns current processed signal
- `get_history()` - returns dict of all named stages
- `reset()` - resets to input signal

## quick example

```python
from prototype import load_audio, save_audio, hard_clip, plot_comparison

fs, signal = load_audio('dry_guitar.wav')
fuzz = hard_clip(signal, gain=20.0, threshold=0.3)
save_audio('fuzz_out.wav', fuzz, fs)
plot_comparison({'input': signal, 'output': fuzz}, fs, save_path='result.png')
```
