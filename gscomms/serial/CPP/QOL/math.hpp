/*
Author: Nicholas Ball

This function will be used to aid in calculating various radio related information

*/

#ifndef MATH_HPP
#define MATH_HPP


// Find a sample rate to use for a given freqency
long long CalculateSampleRate(long long frequency)
{
    long long sample_rate = frequency;

    while(sample_rate > 1e6) sample_rate /= 10;

    return sample_rate;
}

#endif