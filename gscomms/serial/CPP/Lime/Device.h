/*
This header file will hold data to work with lime devices
*/

#include <lime/LimeSuite.h>
#include "../QOL/IQ.h"

#ifndef DEVICE_H
#define DEVICE_H

class Device {
  private:
    // Current Freqency operating on
    long long Freqency;

    // This is the pointer to a current radio device
    lms_device_t* Radio;
    lms_stream_t RX_Stream;
    lms_stream_t TX_Stream;



  public:

    Device ();

    ~Device ();

    //Set Frequency to work on
    bool SetFreqency(long long freq);

    // Disconnect radio
    void Disconnect();

    // Connect to radio
    void Connect();

    // Transmit IQ data
    bool TX(std::vector<IQ>* TX_Buffer);

    // Collect data from Lime device (Returns bool if error happened)
    bool RX(std::vector<IQ>* RX_Buffer,int num_samples);

    // This will open and keep the connection with the radio open
    void Serial_Hack();

    double Get_Sample_Rate();

    //hold thread till radio is setup
    void Wait();


};

#endif
