#include <iostream>
#include <string.h>
#include <vector>
#include <thread>
#include <chrono>
#include <FSK.h>
#include <Device.cpp>
#include <IQ.h>

class Serial
{   private:
        double Freqency;
        std::vector<std::vector<IQ>> rx_buffer;
        std::vector<std::vector<IQ>> tx_buffer;

        // get current epoch in seconds
        static long long GetTimeSec()
        {
            return (long long)(std::chrono::system_clock::now().time_since_epoch().count() / 1000000000);
        }

        // tx loop (run in a new thread)
        static void _tx_loop(Serial *serial)
        {
            // tx loop
            while(true)
            {
                // sync tx time
                while(GetTimeSec() % 10 != 0) {}

                // get from tx buffer
                auto buffer = serial->read_tx_Buffer();

                // if there is something to transmit, send it
                if(buffer.size() > 0) serial->Radio.TX(&buffer);

                // wait to reset till next tx time
                std::this_thread::sleep_for(std::chrono::seconds(1));

            }
        }

        // rx loop (run in a new thread)
        static void _rx_loop(Serial *serial)
        {
            // rx loop
            while(true)
            {
                // sync rx time
                while(GetTimeSec() % 10 != 0) {}

                std::cout<<GetTimeSec()<<std::endl;

                serial->send_to_rx_Buffer({});

                std::this_thread::sleep_for(std::chrono::seconds(1));

            }
            
        }

        // start radio loops
        void start_threads()
        {
            std::thread(_rx_loop, this).detach();
            std::thread(_tx_loop, this).detach();
        }

    protected:
        Device Radio;

        void send_to_rx_Buffer(std::vector<IQ> arr)
        {
            this->rx_buffer.push_back(arr);
        }

        std::vector<IQ> read_tx_Buffer()
        {
            if(this->tx_buffer.size() > 0)
            {
                auto hold = this->tx_buffer[0];

                this->tx_buffer.erase(this->tx_buffer.begin());

                return hold;
            }

            return {};
        }

    public:
        // defualt constructor
        Serial() : Freqency(915e6),tx_buffer({}),rx_buffer({}),Radio(Freqency) {start_threads();}

        // more control constructor
        Serial(double freqency) : Freqency(freqency),tx_buffer({}),rx_buffer({}), Radio(Freqency){start_threads();}

        // send a string for transmission
        bool tx(std::string text);

        // get string from transmission
        std::string rx();
};