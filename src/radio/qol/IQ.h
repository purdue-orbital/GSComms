//
// Created by nicholasball on 1/28/23.
//

#ifndef RADIO_IQ_H
#define RADIO_IQ_H
#include <vector>
#include <math.h>

class IQ
{
public:

    float I,Q;

    IQ(): I(0),Q(0) {};

    IQ(float i, float q) : I(i),Q(q) {}

    void operator=(IQ other)
    {
        this->I = other.I;
        this->Q = other.Q;
    }

    float amplitude()
    {
        return sqrt((I * I) + (Q * Q));
    }

    float distance(IQ other)
    {
        return sqrt(powf(other.I - this->I,2) + powf(other.Q - this->Q,2));
    }

    float phase_shift(IQ other, float freqency)
    {
        return 180 * (this->distance(other) / (1 / freqency));
    }


    // make array of IQ data from float vector
    static std::vector<IQ> from_array(std::vector<float> arr)
    {
        std::vector<IQ> toReturn;
        toReturn.resize((int)(arr.size() / 2));

        // Make IQ data
        for(int i = 0; i < toReturn.size(); i++) toReturn[i] = IQ(arr[2 * i],arr[2 * i + 1]);

        return toReturn;
    }

    // make array of IQ data from float vector
    static std::vector<float> to_array(std::vector<IQ> arr)
    {
        std::vector<float> toReturn;
        toReturn.resize(arr.size() * 2);

        // Make IQ data
        for(int i = 0; i < toReturn.size(); i += 2)
        {
            toReturn[i] = arr[i].I;
            toReturn[i + 1] = arr[i].Q;
        }

        return toReturn;
    }

};
#endif //RADIO_IQ_H
