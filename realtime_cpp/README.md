# Real-Time C++ Guitar Processor

minimal real-time audio processing with low latency

## features

- real-time audio i/o via portaudio
- sample-by-sample processing (~5.8ms latency @ 256 buffer)
- fuzz distortion effect
- lowpass filter for tone control

## current effects

**fuzz** - hard clipping distortion
- gain: 15.0
- threshold: 0.4

**lowpass filter** - tone shaping
- cutoff: 5000 Hz
- Q: 0.707 (butterworth)

## dependencies

```bash
# ubuntu/debian
sudo apt-get install portaudio19-dev

# arch
sudo pacman -S portaudio

# macos
brew install portaudio
```

## build

```bash
make
```

## run

```bash
./guitar_processor
```

connect your guitar to audio input, output goes to speakers/headphones

press enter to stop processing

## structure

```
realtime_cpp/
├── src/
│   ├── main.cpp        # portaudio setup and audio callback
│   ├── effects.h/cpp   # fuzz and biquad filter
│   └── processor.h/cpp # effect chain processor
├── Makefile
└── README.md
```

## adding effects

1. implement effect class in `effects.h/cpp`
2. add to `processor.h/cpp` effect chain
3. rebuild with `make`

## performance

- sample rate: 44100 Hz
- buffer size: 256 samples
- latency: ~5.8ms (1 buffer)
- processing: sample-by-sample (no batch operations)

## future

- add more effects from python prototype
- parameter control via CLI or MIDI
- preset system
- multi-threading for lower latency
