#include <portaudio.h>
#include <iostream>
#include <cstring>
#include "processor.h"

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256

struct audio_data {
    audio_processor* processor;
};

static int audio_callback(const void* input_buffer, void* output_buffer,
                         unsigned long frames_per_buffer,
                         const PaStreamCallbackTimeInfo* time_info,
                         PaStreamCallbackFlags status_flags,
                         void* user_data) {

    const float* input = static_cast<const float*>(input_buffer);
    float* output = static_cast<float*>(output_buffer);
    audio_data* data = static_cast<audio_data*>(user_data);

    if (input == nullptr) {
        memset(output, 0, frames_per_buffer * sizeof(float));
        return paContinue;
    }

    for (unsigned long i = 0; i < frames_per_buffer; i++) {
        output[i] = data->processor->process_sample(input[i]);
    }

    return paContinue;
}

int main() {
    PaError err;
    PaStream* stream;
    audio_processor processor(SAMPLE_RATE);
    audio_data data;
    data.processor = &processor;

    std::cout << "guitar processor - realtime c++ edition\n";
    std::cout << "sample rate: " << SAMPLE_RATE << " Hz\n";
    std::cout << "buffer size: " << FRAMES_PER_BUFFER << " samples\n";
    std::cout << "latency: ~" << (FRAMES_PER_BUFFER * 1000.0 / SAMPLE_RATE) << " ms\n\n";

    err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "portaudio error: " << Pa_GetErrorText(err) << "\n";
        return 1;
    }

    err = Pa_OpenDefaultStream(&stream,
                               1,
                               1,
                               paFloat32,
                               SAMPLE_RATE,
                               FRAMES_PER_BUFFER,
                               audio_callback,
                               &data);

    if (err != paNoError) {
        std::cerr << "portaudio error: " << Pa_GetErrorText(err) << "\n";
        Pa_Terminate();
        return 1;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "portaudio error: " << Pa_GetErrorText(err) << "\n";
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 1;
    }

    std::cout << "processing audio... press enter to stop\n";
    std::cin.get();

    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << "portaudio error: " << Pa_GetErrorText(err) << "\n";
    }

    Pa_CloseStream(stream);
    Pa_Terminate();

    std::cout << "stopped\n";

    return 0;
}
