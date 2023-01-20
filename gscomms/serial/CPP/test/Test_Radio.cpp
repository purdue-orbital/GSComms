/*
    This file will test the radio with communication with itself



*/

#include <iostream>
#include <fstream>
#include <serial.h>


int main()
{
                          
    try{
 
        // start radio
        Serial radio(915e6);

        while(true){}

        

    }catch(const char* ex)
    {
        // open file
        std::ofstream file("Radio_LOG.txt");

        // write error to file
        file << ex;

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;

    } catch (...){

        // open file
        std::ofstream file("Radio_LOG.txt");

        // write error to file
        file << "runtime error";

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;
    }

    return 0;
}
