/*
This header file will preform BPSK on a set of data
*/
#include <string.h>
#include "../QOL/IQ.h"
#include <math.h>
#include <vector>

#ifndef BPSK_H
#define BPSK_H

class BPSK {
public:
    BPSK();
    static std::vector<IQ> Mod(std::string bin, double sample_rate, double freqency)
    {
      std::vector<IQ> toReturn = {};

      // bpsk removes the first number so we add it back here
      bin = "0"+bin;

      // calculate phi
      double phi = 2 * M_PI * freqency;

      // make a basic, continous wave
      for(int i = 0; i != bin.size();i++)
      {
        // create IQ data
        IQ temp(sin(phi * (i / sample_rate) + ((bin[i] == '1') * M_PI)),cos(phi * (i / sample_rate) + ((bin[i] == '1') * M_PI)));

        // add IQ data point to wave
        toReturn.push_back(temp);
      }

      return toReturn;
    }

    static std::string Demod(std::vector<IQ> bin)
    {
      std::string toReturn = "";
      bool one = false;

      for(int i = 1; i != bin.size();i++){
        // Calculate distance
        double x = (bin[i].I - bin[i-1].I) * (bin[i].I - bin[i-1].I);
        double y = (bin[i].Q - bin[i-1].Q) * (bin[i].Q - bin[i-1].Q);
        double distance = sqrt(x + y);

        //std::cout<<bin[i].Amplitude()<<std::endl;

        // if distance is greater than 1, flip value
        if(bin[i].Amplitude() > 0.3)
        {
          if(distance >= 0.5) one = !one;
          toReturn += std::to_string((int)one);
        }

        //std::cout<<distance<<std::endl;

      }

      return toReturn;
    }


};

#endif
