#include "../src/radio/factory/Modulator.h"
#include <iostream>


int main()
{
    Modulator mod(10e6,30e3,100e3);
    std::string out = mod.Demod(mod.Mod("01101010110001101101111110000000011101010010100"));

    if(out == "01101010110001101101111110000000011101010010100")
    {
        std::cout<<"Modulation: PASSED"<<std::endl;
    }else{
        std::cout<<"Modulation: FAILED"<<std::endl;
    }

    std::cout<<"Out: "<<out<<std::endl;

    return 0;
}