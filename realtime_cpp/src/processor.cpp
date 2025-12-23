#include "processor.h"

audio_processor::audio_processor(float sample_rate)
    : sample_rate_(sample_rate)
    , fuzz_(15.0f, 0.4f)
    , fuzz_enabled_(true)
    , filter_enabled_(true) {

    filter_.set_lowpass(sample_rate_, 5000.0f);
}

float audio_processor::process_sample(float input) {
    float output = input;

    if (fuzz_enabled_) {
        output = fuzz_.process_sample(output);
    }

    if (filter_enabled_) {
        output = filter_.process_sample(output);
    }

    return output;
}

void audio_processor::set_fuzz_enabled(bool enabled) {
    fuzz_enabled_ = enabled;
}

void audio_processor::set_filter_enabled(bool enabled) {
    filter_enabled_ = enabled;
}
