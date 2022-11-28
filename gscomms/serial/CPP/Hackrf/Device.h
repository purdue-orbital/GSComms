
/*
This header file will hold data to work with lime devices
*/

#include <libhackrf/hackrf.h>

#ifndef DEVICE_H
#define DEVICE_H

class Device {
  private:
    // Current Freqency operating on
    long long Freqency;

    // This is the pointer to a current radio device
    hackrf_device* Radio;

    bool Mux;


  public:

    Device ();

    ~Device ();

    //Set Frequency to work on
    bool SetFreqency(long long freq);

    // Disconnect radio
    void Disconnect();

    // Connect to radio
    void Connect();

    // Collect data from Lime device (Returns bool if error happened)
    bool TX(std::vector<IQ>* TX_Buffer);

    bool RX(std::vector<IQ>* RX_Buffer,float sleep_nanoseconds);

};

#endif
