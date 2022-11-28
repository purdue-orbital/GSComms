#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif
#include <iostream>
#include <math.h>
#include <cstdint>
#include <cstring>

#include "../QOL/IQ.h"
#include "Device.h"

// global buffer as a read buffer
std::vector<IQ> __Read_Buffer__ = {};

// this function will handle rx calls
int rx_callback(hackrf_transfer* transfer){

  // convert data to IQ values
  for(int i = 0; i != transfer->buffer_length / 2;i++){
    //put IQ value into array
    __Read_Buffer__.push_back(IQ(((int)transfer->buffer[2*i]-128) / 128 ,((int)transfer->buffer[2*i+1] - 128) / 128));

    std::cout<<(int)transfer->buffer[2*i]<<" ";
  }
  std::cout<<std::endl;

  return 0;
}

// this function will handle rx calls
int tx_callback(hackrf_transfer* transfer){

  //make sure buffer isn't blank
  if(__Read_Buffer__.size() == 0)
  {
    return -1;
  }

  //set data in buffer
  for(int i = 0; i != __Read_Buffer__.size();i++)
  {
    //set buffer
    transfer->buffer[2*i] = (__Read_Buffer__[i].I + 1) * 255;
    transfer->buffer[2*i+1] = (__Read_Buffer__[i].Q + 1) * 255;
  }

  //set buffer size
  transfer->buffer_length = __Read_Buffer__.size() * 2;

  __Read_Buffer__ = {};

  return 0;
}

// Constructor
Device::Device()
{
  //var for catching errors
  int err;

  // Init. hackrf lib
  err = hackrf_init();

  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Starting Hackrf: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is everything installed properly?)"<<std::endl;
  }

  // Get list of hackrf devices
  auto list = hackrf_device_list();

  // Open Hackrf
  err = hackrf_open(&Radio);

  //check for error
  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Opening Hackrf: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is the radio connected?)"<<std::endl;
  }

  // Set Ssmple rate
  err = hackrf_set_sample_rate(Radio, 32e3);

  //check for error
  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Setting sample rate: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is the sample rate to high/low?)"<<std::endl;
  }

}

// Deconstructor
Device::~Device()
{
  hackrf_close(Radio);
  hackrf_exit();
}


bool Device::RX(std::vector<IQ>* RX_Buffer,float sleep_nanoseconds){

  //blank out read_buffer
  __Read_Buffer__ = {};

	int err = hackrf_set_vga_gain(Radio, 20);
	err |= hackrf_set_lna_gain(Radio, 8);

	err |= hackrf_start_rx(Radio,rx_callback,NULL);

  //check for error
  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Reading from Hackrf: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is the data being passed correct)"<<std::endl;
    return true;
  }

  //wait for hackrf to collect data
  usleep(sleep_nanoseconds);

  // stop stream
  hackrf_stop_rx(Radio);

  // Return buffer
  *RX_Buffer = __Read_Buffer__;
  std::cout<<RX_Buffer->size()<<std::endl;

  return false;


}

bool Device::TX(std::vector<IQ>* TX_Buffer){
  int err = hackrf_set_txvga_gain(Radio, 0);
  //check for error
  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Reading from Hackrf: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is the data being passed correct)"<<std::endl;
    return true;
  }

  err = hackrf_start_tx(Radio,tx_callback,NULL);

  //set data into buffer
  __Read_Buffer__ = *TX_Buffer;

  //check for error
  if(err != HACKRF_SUCCESS){
    std::cout<<"Error Reading from Hackrf: '"<<hackrf_error_name((hackrf_error)err)<<"' (Is the data being passed correct)"<<std::endl;
    return true;
  }

  // stop stream
  hackrf_stop_tx(Radio);

  return false;


}
