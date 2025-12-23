#include "effects.h"
#include <cmath>
#include <algorithm>

fuzz_effect::fuzz_effect(float gain, float threshold)
    : gain_(gain), threshold_(threshold) {}

float fuzz_effect::process_sample(float input) {
    float boosted = input * gain_;
    float clipped = std::max(-threshold_, std::min(threshold_, boosted));
    return clipped / threshold_;
}

void fuzz_effect::set_gain(float gain) {
    gain_ = gain;
}

void fuzz_effect::set_threshold(float threshold) {
    threshold_ = threshold;
}

biquad_filter::biquad_filter()
    : b0_(1.0f), b1_(0.0f), b2_(0.0f)
    , a1_(0.0f), a2_(0.0f)
    , x1_(0.0f), x2_(0.0f)
    , y1_(0.0f), y2_(0.0f) {}

void biquad_filter::set_lowpass(float sample_rate, float cutoff_freq) {
    float w0 = 2.0f * M_PI * cutoff_freq / sample_rate;
    float cos_w0 = std::cos(w0);
    float sin_w0 = std::sin(w0);
    float alpha = sin_w0 / (2.0f * 0.707f);

    float a0 = 1.0f + alpha;
    b0_ = ((1.0f - cos_w0) / 2.0f) / a0;
    b1_ = (1.0f - cos_w0) / a0;
    b2_ = ((1.0f - cos_w0) / 2.0f) / a0;
    a1_ = (-2.0f * cos_w0) / a0;
    a2_ = (1.0f - alpha) / a0;
}

float biquad_filter::process_sample(float input) {
    float output = (b0_ * input) + (b1_ * x1_) + (b2_ * x2_)
                   - (a1_ * y1_) - (a2_ * y2_);

    x2_ = x1_;
    x1_ = input;
    y2_ = y1_;
    y1_ = output;

    return output;
}

void biquad_filter::reset() {
    x1_ = x2_ = 0.0f;
    y1_ = y2_ = 0.0f;
}
