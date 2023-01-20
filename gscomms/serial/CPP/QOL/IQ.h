#include <iostream>
#include <vector>
#include <math.h>
#include <array>

#ifndef IQ_H
#define IQ_H

class IQ {
  public:
    // I and Q componets of IQ data
    double I;
    double Q;

    // Set vars individually
    IQ(double i,double q){I = i; Q = q;}

    IQ(const IQ &data){I = data.I; Q = data.Q;}

    IQ(IQ *data){I = data->I; Q = data->Q;}

    // get amplitude of IQ
    double Amplitude(){
      return sqrt((I * I) + (Q * Q));
    }

    // get the phase angle of IQ data from 0 to 2pi
    double Phase(){
      return  (I / abs(I)) * atan(Q / I);
    }

    // This will return adjust values used to convert normilized data back to normal data
    std::array<double, 2> Unnormalize(double num)
    {
      return {I * num, Q * num};
    }

    // calculate the phase shift
    double PhaseShift(IQ other_data){
      return fabs(this->Phase() - other_data.Phase());
    }

    // calculate the distance of two IQ points
    double Distance(IQ other_data)
    {
      return sqrt(((this->I + other_data.I)*(this->I + other_data.I)) + ((this->Q + other_data.Q)*(this->Q + other_data.Q)));
    }

    // (DEPRECATED) return an array of IQ data from a 2d array
    static std::vector<IQ> from_array(double* arr,int size){
      //make array of IQ data
      std::vector<IQ> toReturn = {};

      // loop through data
      for(int i = 0; i < size; i += 2)
      {
        // add item to array
        toReturn.push_back(IQ(arr[i],arr[i+1]));
      }

      // return array
      return toReturn;

    }

};

#endif
