#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
//#include "Hackrf/Device.cpp"
#include "Modulation/FSK.h"




int main(){
  double freqency = 916e6;
  double sample_rate = 32e3;

  auto out = FSK::Mod(std::string("000111000111000"),sample_rate,freqency);

  Device d;
  while(true)
  {
    d.TX(&out);
  }


  return 0;
}
