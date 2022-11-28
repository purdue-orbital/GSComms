/*
This header file will preform BPSK on a set of data
*/
#include <string.h>
#include "../QOL/IQ.h"
#include <math.h>
#include <vector>

int Margin = 100;

#ifndef BPSK_H
#define BPSK_H

class BPSK {
public:
    BPSK();
    static std::vector<IQ> Mod(std::string bin,double sample_rate,double freqency)
    {
      std::vector<IQ> out = {};

      //loop through bin and modulate values
      for(int i = 0; i != bin.length();i++)
      {
        double offset = bin[i] == '1';

        //loop through bin and modulate values
        for(int i = 0; i != Margin;i++)
        {
          double phi = 2 * M_PI * freqency * (i / sample_rate);
          out.push_back(IQ(cos(phi + (3.14 * offset)),sin(phi + (3.14 * offset))));
        }
      }
      return out;
    }

    static std::string Demod(std::vector<IQ> bin)
    {
      double diff  = 0;
      std::string out = "";
      bool one = true;

      // find the difference of adjust phases and build binary
      for(int i = 0; i <= bin.size()-1;i++)
      {
        //flip bits when the phases are about 0 in differnce
        if(bin[i].PhaseShift(bin[i+1]) > 2) one = !one;

        //add bit to string of nums
        if(one) out += "1";
        else out += "0";
      }

      std::string hold = "";
      // only use every margin number of bits
      for(int i = 0; i <= out.length();i += Margin)
      {
        hold += out[i];
      }

      return hold;
    }


};

#endif
