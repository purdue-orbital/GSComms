/*
    This file tests if Viterbi works with itself.

    If this passes, the script will print "PASSED"

    If it does not pass, the script will print "FAILED"
*/

#include <iostream>
#include <fstream>
#include <viterbi.cpp>


int main()
{
    try{
        ViterbiCodec codec(3,{7,5});

        if(codec.Decode(codec.Encode("10011001110001000111110101010")) == "10011001110001000111110101010") std::cout<<"PASSED"<<std::endl;
        else throw "Viterbi did not properly encode and decode string";

    }catch(const char* ex)
    {
        // open file
        std::ofstream file("Viterbi_LOG.txt");

        // write error to file
        file << ex;

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;

    } catch (...){

        // open file
        std::ofstream file("Viterbi_LOG.txt");

        // write error to file
        file << "runtime error";

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;
    }

    return 0;
}