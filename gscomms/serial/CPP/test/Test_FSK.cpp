/*
    This file tests if FSK works with itself.

    If this passes, the script will print "PASSED"

    If it does not pass, the script will print "FAILED"
*/

#include <iostream>
#include <fstream>
#include <FSK.h>


int main()
{                               

    try{
        if(FSK::Demod(FSK::Mod("10011001110001000111110101010",32e3,915e6)) == "10011001110001000111110101010") std::cout<<"PASSED"<<std::endl;
        else throw "FSK did not properly modulate and demodulate string";

    }catch(const char* ex)
    {
        // open file
        std::ofstream file("FSK_LOG.txt");

        // write error to file
        file << ex;

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;

    } catch (...){

        // open file
        std::ofstream file("FSK_LOG.txt");

        // write error to file
        file << "runtime error";

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;
    }

    return 0;
}