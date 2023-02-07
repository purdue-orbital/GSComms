#include "../src/radio/factory/DataLine.h"
#include "../src/radio/factory/Modulator.h"
#include <iostream>


int main()
{
    double radio_freqency = 915e6;
    double radio_sample_rate = 2e6;
    double radio_bandwidth = 50e3;
    double tone_freqency = 60e3;
    double modulation_sample_rate = 10e3;

    Modulator m(radio_sample_rate, tone_freqency, modulation_sample_rate);

    DataLine dl(radio_freqency,radio_sample_rate,radio_bandwidth);

    std::cout<<"Transmitting!"<<std::endl;

    //while(true) {
        dl.Transmit(m.Mod("001010001101101"));
        //std::this_thread::sleep_for(std::chrono::milliseconds (100));
   //}
    std::cout<<"Fetching!"<<std::endl;
    auto out = m.Demod(dl.Fetch());

    std::cout<<out<<std::endl;
    //while (true)
    //{
        std::this_thread::sleep_for(std::chrono::milliseconds (5000));
        std::cout<<(out.find("001010001101101") < 1e9 )<<std::endl;
    //}


    std::cout<<"Fin!"<<std::endl;

    return 0;
}