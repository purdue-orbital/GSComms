/*
This header file will preform BPSK on a set of data
*/
#include <string.h>
#include "../QOL/IQ.h"
#include <math.h>
#include <vector>

int Margin = 1;

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
          double phi = 2 * M_PI * (freqency + (10000 * offset)) * (( (Margin * i) + k) / sample_rate);
          out.push_back(IQ(cos(phi),sin(phi)));
        }
      }
      return out;
    }

    static std::vector<std::string> Demod(std::vector<IQ> bin)
    {
      std::vector<std::string> toReturn = {};
      std::vector<IQ> temp1 = {};
      std::vector<std::vector<IQ>> temp2 = {bin};

      /*
      // filter and breakup noise
      for(int y = 0; y != bin.size();y++)
      {
        IQ check = bin[y];

        if(check.Amplitude() > 0.3){
          temp1.push_back(check);
        }else if(temp1.size() > 0){
          temp2.push_back(temp1);
          temp1 = {};
        }
      }

      if(temp1.size() > 0){
          temp2.push_back(temp1);
          temp1 = {};
      }
      */

      //loop through each broken up segment
      for(int y = 0; y != temp2.size();y++)
      {
        std::string out = "";

        // find where the rate changes
        for(int i = 0; i <= temp2[y].size()-1;i++)
        {
          //std::cout<< temp2[y][i].PhaseShift(bin[i+1]) <<std::endl;
          //add bit to string of nums
          if(bin[i].PhaseShift(temp2[y][i+1]) > 1) out += "1";
          else out += "0";
        }

        std::string hold = "";

        // only use every margin number of bits
        for(int i = 0; i <= out.length();i += Margin)
        {
          hold += out[i];
        }

        toReturn.push_back(hold);
      }

      return toReturn;
    }


};

#endif
