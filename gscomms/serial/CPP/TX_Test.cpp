#include <iostream>
#include <math.h>
#include "Lime/Device.cpp"
#include "QOL/viterbi.cpp"
#include "QOL/math.hpp"
//#include "Hackrf/Device.cpp"
#include "Modulation/BPSK.h"




int main(){
  double freqency = 915e6;
  double sample_rate = CalculateSampleRate(freqency);


  auto codec = ViterbiCodec(3,{7,5});

  auto text = codec.Encode("001010000000");

  srand (time(NULL));

  /*

  // flip random bits
  for(int i = 0; i < text.size() / 4;i++)
  {
    int index = rand() % text.size();

    text = text.substr(0,index) + std::to_string(text[i] == '0') + text.substr(index+1);
  }

  */

  auto out = BPSK::Mod(std::string(text),sample_rate,freqency);


  std::string nothing = "";

  auto out2 = BPSK::Demod(out);

  std::cout<<codec.Decode(out2)<<std::endl;

  /**/
  Device d;
  while(true)
  {

    out = BPSK::Mod(std::string(text),sample_rate,freqency);
    std::cout<<"Press enter to send!: ";

    std::cin >> nothing;
    std::cout<<"Transmitting!\n"<<std::endl;

    for(int i = 0; i != 10;i++)
    {
      d.TX(&out);
    }


  }
  /**/


  return 0;
}
