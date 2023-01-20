/*
FSK is modulation method that varries the frequency of the transmission to create binary data

EX: 101 -> higher frequency,base freqency,higher frequency

*/
#include <string.h>
#include <IQ.h>
#include <math.h>
#include <vector>
#include <iostream>

int Margin = 1;

#ifndef FSK_H
#define FSK_H

class FSK {
public:
    FSK();
    static std::vector<IQ> Mod(std::string bin,double sample_rate,double freqency)
    {
      std::vector<IQ> out = {};

      bin = "0000" + bin;

      //loop through bin and modulate values
      for(int i = 0; i != bin.length();i++)
      {
        // calculate phi
        double phi = 2 * M_PI * (freqency + (333 * (bin[i] == '1'))) * (i / sample_rate) + M_PI;

        // make iq point
        IQ temp(sin(phi),cos(phi));

        // add to array
        out.push_back(temp);

      }
      return out;
    }

    static std::string Demod(std::vector<IQ> bin)
    {
      std::string toReturn = "";

      // we assume first two points are in sync with each other and is zero
      double BaseDistance = bin[0].Distance(bin[1]);
      auto _temp = "000010011001110001000111110101010";

      bool one = false;

      // loop through IQ points
      for(int i = 1; i != bin.size()-1;i++)
      {
        auto diff = fabs(bin[i].Distance(bin[i+1]) - BaseDistance);
        if(diff > 0.1) one = !one;

        toReturn += std::to_string(one);
      }


      return toReturn.substr(2);
    }


};

#endif
