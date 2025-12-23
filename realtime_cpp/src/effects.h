#ifndef EFFECTS_H
#define EFFECTS_H

class fuzz_effect {
public:
    fuzz_effect(float gain = 10.0f, float threshold = 0.5f);

    float process_sample(float input);

    void set_gain(float gain);
    void set_threshold(float threshold);

private:
    float gain_;
    float threshold_;
};

class biquad_filter {
public:
    biquad_filter();

    void set_lowpass(float sample_rate, float cutoff_freq);
    float process_sample(float input);
    void reset();

private:
    float b0_, b1_, b2_;
    float a1_, a2_;

    float x1_, x2_;
    float y1_, y2_;
};

#endif
