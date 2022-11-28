#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
//#include "Hackrf/Device.cpp"
#include "Modulation/BPSK.h"




int main(){
  double freqency = 916e6;
  double sample_rate = 32e3;
  std::vector<IQ> out = {};

  out = BPSK::Mod(std::string("000101000"),sample_rate,freqency);

  Device d;

  while(true)
  {
    d.RX(&out,1000000);
    std::cout<<out.size()<<std::endl;
    std::cout<<BPSK::Demod(out)<<std::endl;
  }



  return 0;
}
