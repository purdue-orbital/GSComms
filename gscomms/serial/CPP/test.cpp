#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
#include "Modulation/BPSK.h"




int main(){
  double freqency = 916e6;
  double sample_rate = 32e3;

  auto out = BPSK::Mod(std::string("000111000"),sample_rate,freqency);
  for(int x = 0; x != out.size();x++)
  {
    //std::cout<<out[x].I<<std::endl;
  }

  Device d;
  d.Wait();
  d.TX(&out);
  d.RX(&out,10000);


  std::cout<<BPSK::Demod(out)<<std::endl;




  return 0;
}
