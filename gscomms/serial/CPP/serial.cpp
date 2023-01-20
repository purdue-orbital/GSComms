#include <iostream>
#include <FSK.h>
#include <serial.h>
#include <math.hpp>

std::string Serial::rx()
{
    if (this->rx_buffer.size() > 0) {

        // get buffer
        auto buffer = this->rx_buffer[0];

        // pop stack
        this->rx_buffer.erase(this->rx_buffer.begin());

        // demod
        auto f = FSK::Demod(buffer);

        return f;
    }
    
    return "";
}

bool Serial::tx(std::string text)
{
    try{
        // modulate and send to buffer
        this->tx_buffer.push_back(FSK::Mod(text,CalculateSampleRate(this->Freqency),Freqency));

    }catch(...)
    {
        return false;
    }
    return true;
}