#ifndef PROCESSOR_H
#define PROCESSOR_H

#include "effects.h"

class audio_processor {
public:
    audio_processor(float sample_rate);

    float process_sample(float input);

    void set_fuzz_enabled(bool enabled);
    void set_filter_enabled(bool enabled);

    fuzz_effect& get_fuzz() { return fuzz_; }
    biquad_filter& get_filter() { return filter_; }

private:
    float sample_rate_;

    fuzz_effect fuzz_;
    biquad_filter filter_;

    bool fuzz_enabled_;
    bool filter_enabled_;
};

#endif
