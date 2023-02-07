//
// Created by nicholasball on 2/5/23.
//

#include "../src/radio/factory/DataLine.h"
#include "../src/radio/factory/Modulator.h"
#include <iostream>


int main()
{
    double radio_freqency = 915e6;
    double radio_sample_rate = 2e6;
    double radio_bandwidth = 300e3;
    double tone_freqency = 60e3;
    double modulation_sample_rate = 180e3;

    Modulator m(radio_sample_rate, tone_freqency, modulation_sample_rate);

    DataLine dl(radio_freqency,radio_sample_rate,radio_bandwidth);

    while (true)
    {
        auto out = m.Mod("001010001101101");
        dl.Transmit(out);
    }

    return 0;
}