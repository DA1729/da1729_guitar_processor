# Guitar Processor

digital signal processing library for guitar effects

## overview

python-based guitar effects processor with production-ready DSP algorithms. supports offline processing, effect chaining, and includes analysis tools for algorithm development.

## project structure

```
guitar_processor/
├── logic_model/        # experimental DSP algorithms (rough work)
├── prototype/          # production-ready python library
├── realtime_cpp/       # real-time c++ processor
└── README.md           # this file
```

**logic_model/** - algorithm prototyping and validation
- individual effect scripts
- visualization and analysis
- reference implementations

**prototype/** - structured python package
- modular effect library
- clean API with documentation
- effect chaining processor

**realtime_cpp/** - real-time audio processing
- low-latency c++ implementation
- portaudio for audio i/o
- sample-by-sample processing

## setup

```bash
# create virtual environment
python3 -m venv ~/venv
source ~/venv/bin/activate

# install dependencies
pip install numpy scipy matplotlib
```

## progress

- audio i/o with normalization
- distortion effects (fuzz, overdrive)
- delay/echo effect
- cabinet simulation with IR convolution
- dynamics processing (compressor, noise gate)
- biquad filters (lowpass, highpass, bandpass)
- time/frequency domain analysis
- effect chaining via processor class

## structure

```
prototype/
├── audio_io.py     # load/save/normalize audio
├── effects.py      # guitar effects
├── filters.py      # biquad filters
├── dynamics.py     # compressor, gate
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

**cabinet** - speaker cabinet simulation using impulse response convolution
- `ir` (default: None) - custom impulse response array, None = use synthetic IR
- `duration_ms` (default: 20) - synthetic IR duration, only used if ir=None

**generate_cab_ir** - creates synthetic cabinet impulse response
- `fs` - sample rate
- `duration_ms` (default: 20) - IR length in milliseconds

### dynamics

```python
from prototype import compressor, noise_gate

compressed = compressor(signal, fs, threshold_db=-20.0, ratio=4.0,
                        attack_ms=5.0, release_ms=50.0, makeup_gain_db=5.0)
gated = noise_gate(signal, fs, threshold_db=-40.0, attack_ms=2.0,
                   release_ms=100.0, hold_ms=10.0)
```

**compressor** - dynamic range compression, evens out volume
- `threshold_db` (default: -20.0) - level where compression starts, lower = more compression
- `ratio` (default: 4.0) - compression amount, higher = more squashing (1.0=off, 20.0=limiting)
- `attack_ms` (default: 5.0) - how fast compression engages, lower = faster
- `release_ms` (default: 50.0) - how fast compression releases, higher = smoother
- `makeup_gain_db` (default: 5.0) - output boost to compensate volume loss

**noise_gate** - removes noise during silence, cuts signal below threshold
- `threshold_db` (default: -40.0) - noise floor cutoff, signals below this get muted
- `attack_ms` (default: 2.0) - gate opening speed, lower = faster
- `release_ms` (default: 100.0) - gate closing speed, higher = smoother fade
- `hold_ms` (default: 10.0) - minimum time gate stays open

**compute_envelope** - envelope follower utility (used internally)
- `signal` - input audio array
- `fs` - sample rate
- `attack_ms` - attack time
- `release_ms` - release time

### filters

```python
from prototype import lowpass, highpass, bandpass, biquad

lp_signal = lowpass(signal, fs, cutoff_freq=800.0, order=2)
hp_signal = highpass(signal, fs, cutoff_freq=100.0, order=2)
bp_signal = bandpass(signal, fs, low_freq=300.0, high_freq=3000.0, order=2)
custom = biquad(signal, b0, b1, b2, a1, a2)
```

**lowpass** - butterworth lowpass filter, removes high frequencies
- `cutoff_freq` (default: 800.0) - frequency in Hz, above this gets attenuated
- `order` (default: 2) - filter steepness, higher = sharper rolloff

**highpass** - butterworth highpass filter, removes low frequencies
- `cutoff_freq` (default: 800.0) - frequency in Hz, below this gets attenuated
- `order` (default: 2) - filter steepness, higher = sharper rolloff

**bandpass** - butterworth bandpass filter, keeps frequency range
- `low_freq` (default: 300.0) - lower cutoff in Hz
- `high_freq` (default: 3000.0) - upper cutoff in Hz
- `order` (default: 2) - filter steepness, higher = sharper rolloff

**biquad** - direct biquad filter implementation
- `b0, b1, b2` - feedforward coefficients
- `a1, a2` - feedback coefficients

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

## development workflow

1. prototype new effects in `logic_model/` (experimental, rough code)
2. test and validate with plots and audio output
3. port working effects to `prototype/` (clean, documented, production-ready)
4. update this README with new effect documentation

## roadmap

**immediate:**
- modulation effects (chorus, phaser, flanger, tremolo)
- reverb (spring, plate, hall)
- eq and tone shaping (parametric eq, wah)

**future:**
- real-time audio processing
- GUI for parameter control
- preset management
- additional distortion types
- pitch effects (octaver, harmonizer)
