#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
#include "Modulation/FSK.h"




int main(){
  double freqency = 916e6;
  double sample_rate = 32e3;

  auto out = FSK::Mod(std::string("000101000"),sample_rate,freqency);
  for(int x = 0; x != out.size();x++)
  {
    //std::cout<<out[x].I<<std::endl;
  }

  Device d;
  d.Wait();
  d.TX(&out);
  d.RX(&out,10000);


  std::cout<<FSK::Demod(out)<<std::endl;




  return 0;
}
