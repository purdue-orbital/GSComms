//
// Created by nicholasball on 1/26/23.
//

#ifndef RADIO_MODULATOR_H
#define RADIO_MODULATOR_H

#include <iostream>
#include <string>
#include <vector>
#include <math.h>
#include "../qol/IQ.h"

class Modulator
{
private:
    // data
    long long Radio_Sample_Rate;
    long long Tone_Freqency;
    long long Modulation_Sample_Rate;
    long long Margin;
    double FRatio;

    const double pi = acos(-1);



    /*!
     * Modulate bit for fsk
     *
     * @param bit Char bit to modulate (either '1' or '0')
     * @param offset The number of bits made prior (EX: if on 2nd bit set this as 1)
     * @return modulated bits
     */
    std::vector<IQ> FSK_MOD(char bit, int offset = 0)
    {
        std::vector<IQ> toReturn;
        toReturn.resize(Margin);

        return toReturn;
    }

    char FSK_DEMOD(std::vector<IQ> data)
    {

    }

    std::vector<IQ> BPSK_MOD(char bit, int offset = 0)
    {
        // allocate memory
        std::vector<IQ> toReturn;
        toReturn.resize(Margin);

        // find first set of phi
        double w = 2 * pi * FRatio;

        for(int y = 0; y < Margin; y++ )
        {
            // calculate phi
            double phi = (w * ((offset * Margin) + y)) + (pi * (int)(bit == '1'));

            // set IQ data
            toReturn[y] = IQ(cos(phi),sin(phi));
        }

        // return
        return toReturn;
    }


    char BPSK_DEMOD(std::vector<IQ> data, int offset = 0)
    {
        // allocate memory
        float avg = 0;

        // find first set of phi
        double w = 2 * pi * FRatio;

        for(int y = 0; y < Margin; y++ )
        {
            double phi = (w * ((offset * Margin) + y));

            avg += data[y].I - cos(phi);
        }

        std::cout<<avg<<std::endl;

        if(fabs(avg) > 100) return '1';
        return '0';
    }

public:

    Modulator(long long radio_sample_rate, long long tone_freq, long long mod_sample_rate) : Radio_Sample_Rate(radio_sample_rate), Tone_Freqency(tone_freq), Modulation_Sample_Rate(mod_sample_rate)
    {
        FRatio = tone_freq / radio_sample_rate;
        Margin = (long long)(radio_sample_rate / mod_sample_rate);
    }

    std::string Demod(std::vector<float> data)
    {
        auto lazy = IQ::from_array(data);

        std::string out = "";

        for(int y = 0; y < lazy.size(); y += Margin)
        {
            out += BPSK_DEMOD(std::vector<IQ>(lazy.begin() + y,lazy.begin() + y + Margin),y);
        }

        return out.substr(out.size()/2);

    }

    std::vector<float> Mod(std::string bin)
    {

        std::vector<float> tx_buffer;
        tx_buffer.resize((long long)(2 * bin.size() * Margin));


        for (int x = 0; x < bin.size(); x++) {

            auto data = BPSK_MOD(bin[x],x);

            auto formated = IQ::to_array(data);

            tx_buffer.insert(tx_buffer.end(),formated.begin(),formated.end());
        }

        return tx_buffer;
    }
};

#endif //RADIO_MODULATOR_H
