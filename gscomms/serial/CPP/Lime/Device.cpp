#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif
#include <iostream>
#include <math.h>
#include <cstdint>
#include <cstring>
#include <thread>
#include "Device.h"
#include "../QOL/math.hpp"

// Close the connection
bool __Close__ = false;

// Ensure connection is established to the radio
bool __Connected__ = false;

void Device::Serial_Hack()
{
  std::cout<<"Setting up!"<<std::endl;

  lms_info_str_t list[8];
  LMS_GetDeviceList(list);

  lms_range_t bandwidth;
  bandwidth.min = 0;
  bandwidth.max = 0;
  bandwidth.step = 1;

  // Open radio and initlize it
  if (LMS_Open(&Radio, list[0], NULL)) std::cout<<"Error opening radio! (Is the radio plugged in?)";
  if (LMS_Init(Radio) != 0) std::cout<<"Error initilizing radio! (Is the radio responsive?)";

  //setup tx
  if (LMS_EnableChannel(Radio, LMS_CH_TX, 0, true) != 0) std::cout<<"Error starting channel! (Is the radio already opened?)";
  if (LMS_SetLOFrequency(Radio, LMS_CH_TX, 0, 915e6) != 0) std::cout<<"Error setting freqency! (Is the freqency out of range?)";
  if (LMS_SetNormalizedGain(Radio, LMS_CH_TX, 0, 5) != 0) std::cout<<"Error setting gain! (Is the gain out of range?)";
  if (LMS_GetAntennaBW(Radio, LMS_CH_TX, 0, 0, &bandwidth) != 0) std::cout<<"Error setting bandwidth! (Is the bandwidth out of range?)";
  if (LMS_SetupStream(Radio, &TX_Stream) != 0) std::cout<<"Error setting up TX Stream!";

  //setup rx
  if (LMS_EnableChannel(Radio, LMS_CH_RX, 1, true) != 0) std::cout<<"Error starting channel! (Is the radio already opened?)";
  if (LMS_SetLOFrequency(Radio, LMS_CH_RX, 1, 915e6) != 0) std::cout<<"Error setting freqency! (Is the freqency out of range?)";
  if (LMS_SetNormalizedGain(Radio, LMS_CH_RX, 1, 5) != 0) std::cout<<"Error setting gain! (Is the gain out of range?)";
  if (LMS_GetAntennaBW(Radio, LMS_CH_RX, 1, 0, &bandwidth) != 0) std::cout<<"Error setting bandwidth! (Is the bandwidth out of range?)";
  if (LMS_SetupStream(Radio, &RX_Stream) != 0) std::cout<<"Error setting up RX Stream!";



  // set sample rate
  if(LMS_SetSampleRate(Radio,CalculateSampleRate(915e6),0) != 0) std::cout<<"Error setting sample rate!";


  LMS_StartStream(&RX_Stream);
  LMS_StartStream(&TX_Stream);


  //calibrate
  LMS_Calibrate(Radio, LMS_CH_TX, 0, 1000, 0);
  LMS_Calibrate(Radio, LMS_CH_RX, 1, 1000, 0);

  __Connected__ = true;


  //keep radio open
  while(!__Close__){}

  __Connected__ = false;


  //close radio
  LMS_Close(Radio);
}

// Constructor
Device::Device()
{

  //setup streams
  TX_Stream.channel = 0;                         //channel number
  TX_Stream.fifoSize = 1024 * 1024;              //fifo size in samples
  TX_Stream.throughputVsLatency = 0.5;             //0 min latency, 1 max throughput
  TX_Stream.dataFmt = lms_stream_t::LMS_FMT_I16; //doubleing point samples
  TX_Stream.isTx = true;                         //TX channel



  //setup streams
  RX_Stream.channel = 1;                         //channel number
  RX_Stream.fifoSize = 1024 * 1024;              //fifo size in samples
  RX_Stream.throughputVsLatency = 0.5;             //0 min latency, 1 max throughput
  RX_Stream.dataFmt = lms_stream_t::LMS_FMT_I16; //doubleing point samples
  RX_Stream.isTx = false;                        //RX channel


  // open radio
  std::thread t(&Device::Serial_Hack,this);
  t.detach();


}

// Deconstructor
Device::~Device()
{
  // stop serial loop
  __Close__ = true;

  LMS_StopStream(&RX_Stream);
  LMS_StopStream(&TX_Stream);

  LMS_DestroyStream(Radio,&RX_Stream);
  LMS_DestroyStream(Radio,&TX_Stream);

  LMS_Close(Radio);
}

bool Device::RX(std::vector<IQ>* RX_Buffer,int num_samples){

  //Blankout the rx buffer
  *RX_Buffer = {};

  // Wait till radio is connected
  while(!__Connected__){}

  int samplesRead;

  // create buffer
  int16_t buffer[num_samples * 2];

  //Receive samples
  samplesRead = LMS_RecvStream(&RX_Stream, buffer, num_samples, 0, 100000000);

  //catch any errors
  if(samplesRead != num_samples)
  {
    std::cout<<"Error reading data from radio! (Is the data being set correctly?)\n\tSamples Read: "<<samplesRead<<std::endl;
    return true;
  }

  //set the rx buffer
  for(int i = 0; i != num_samples; i++){
    int vI = buffer[2*i];
    int vQ = buffer[2*i+1];

    // normalize and send to array
    RX_Buffer->push_back(IQ(((double)vI / 32768),((double)vQ / 32768)));
  }

  return false;
}

bool Device::TX(std::vector<IQ>* TX_Buffer){

  // Wait till radio is connected
  while(!__Connected__){}

  // get the number of smples
  int samples = TX_Buffer->size();

  // create buffer
  int16_t buffer[samples * 2];

  for(int i = 0; i != samples; i++)
  {
    buffer[2*i] = ((*TX_Buffer)[i].I) * 32768;
    buffer[2*i+1] = ((*TX_Buffer)[i].Q) * 32768;
  }

  lms_stream_meta_t tx_metadata; //Use metadata for additional control over sample send function behavior
  tx_metadata.flushPartialPacket = false; //do not force sending of incomplete packet

  //Send samples
  LMS_SendStream(&TX_Stream, buffer, samples, &tx_metadata, 100000000);

  return false;
}

double Device::Get_Sample_Rate()
{

  // Wait till radio is connected
  while(!__Connected__){}

  double* samplerate1 = new double(0);
  double* samplerate2 = new double(0);

  LMS_GetSampleRate(Radio,LMS_CH_TX,0,samplerate1,samplerate2);
  return *samplerate2;
}

void Device::Wait()
{
  while(!__Connected__){}
}
