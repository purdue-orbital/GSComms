/*
    This file tests if BPSK works with itself.

    If this passes, the script will print "PASSED"

    If it does not pass, the script will print "FAILED"
*/

#include <iostream>
#include <stdexcept>
#include <fstream>
#include <math.h>
#include <IQ.h>


int main()
{
    try{
        // test IQ constructors
        IQ data1(sin(M_PI/4),cos(M_PI/4));
        const IQ data2 = &data1;
        IQ data3 = data2;

        // check I and Q values
        if(data1.I != sin(M_PI/4) || data1.Q != cos(M_PI/4)) throw "incorrect I or Q value set for standard constructor (data1)";
        if(data3.I != sin(M_PI/4) || data3.Q != cos(M_PI/4)) throw "incorrect I or Q value set for copy constructors (data3 or data2)";

        // check amplitudes
        if(data1.Amplitude() != 1) throw "incorrect amplitude result for standard constructor (data1)";
        if(data3.Amplitude() != 1) throw "incorrect amplitude result for copy constructors (data3 or data2)";


        // check phases (within 0.001 radians)
        if(fabs(data1.Phase() - (M_PI / 4)) >= 0.001) throw "incorrect phase given for 45 degrees by the standard constructor (data1)";
        if(fabs(data3.Phase() - (M_PI / 4)) >= 0.001) throw "incorrect phase given for 45 degrees by the copy constructors (data3 or data2)";

        // check phase shift
        if(data1.PhaseShift(data3) != 0) throw "incorrect phaseshift result given for input (data1 or data2 or data3)";

        // check unnormilization
        if(data1.Unnormalize(256)[0] != 256 * sin(M_PI/4) || data1.Unnormalize(256)[1] != 256 * cos(M_PI/4) ) throw "incorrect unormilized data given for standard constructor (data1)";
        if(data3.Unnormalize(256)[0] != 256 * sin(M_PI/4) || data3.Unnormalize(256)[1] != 256 * cos(M_PI/4) ) throw "incorrect unormilized data given for copy constructors (data2 or data3)";

        // flip values for data1
        data1.I *= -1;
        data1.Q *= -1;

        // check phases (within 0.001 radians)
        if(fabs(data1.Phase() + (M_PI / 4)) >= 0.001) throw "incorrect phase given for 225 degrees by the standard constructor (data1)";

        // check phase shift with different phases
        data3.I = sin(0);
        data3.Q = cos(0);

        if((data1.PhaseShift(data3) -  (M_PI / 4)) >= 0.001) throw "incorrect phaseshift result given for 45 degree phase shift (data1 or data3)";

        // if program made it here, test passed
        std::cout<<"PASSED"<<std::endl;

    }catch(const char* ex)
    {
        // open file
        std::ofstream file("IQ_LOG.txt");

        // write error to file
        file << ex;

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;

    } catch (...){

        // open file
        std::ofstream file("IQ_LOG.txt");

        // write error to file
        file << "runtime error";

        // close file
        file.close();

        std::cout<<"FAILED"<<std::endl;
        throw;
    }

    return 0;
}