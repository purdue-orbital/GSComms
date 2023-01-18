#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
#include "QOL/viterbi.cpp"
#include "QOL/math.hpp"

//#include "Hackrf/Device.cpp"

#include "Modulation/BPSK.h"




int main(){
  std::vector<IQ> out = {};

  auto codec = ViterbiCodec(3,{7,5});

  /**/
  Device d;

  while(true)
  {
    // collect
    d.RX(&out,1000000);

    // demodulate
    auto data = BPSK::Demod(out);


    if(data.size() > 0)
    {
      // correct any errors
      std::cout<<codec.Decode(data)<<std::endl;
    }

  }
  /**/



  return 0;
}
