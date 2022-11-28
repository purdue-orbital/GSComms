/*
This header file will preform BPSK on a set of data
*/
#include <string.h>
#include "../QOL/IQ.h"
#include <math.h>
#include <vector>

int Margin = 100;

#ifndef FSK_H
#define FSK_H

class FSK {
public:
    FSK();
    static std::vector<IQ> Mod(std::string bin,double sample_rate,double freqency)
    {
      std::vector<IQ> out = {};

      //loop through bin and modulate values
      for(int i = 0; i != bin.length();i++)
      {
        double offset = bin[i] == '1';

        //loop through bin and modulate values
        for(int k = 0; k != Margin;k++)
        {
          double phi = 2 * M_PI * (freqency + (1000 * offset)) * (( (Margin * i) + k) / sample_rate);
          out.push_back(IQ(cos(phi),sin(phi)));
        }
      }
      return out;
    }

    static std::string Demod(std::vector<IQ> bin)
    {
      double diff  = 0;
      std::string out = "";
      bool one = true;

      // find where the rate changes
      for(int i = 0; i <= bin.size()-1;i++)
      {
        //add bit to string of nums
        if(bin[i].PhaseShift(bin[i+1]) > 0.01) out += "1";
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
