/*
This file will go through each test file

If the test passes, the program will print *TEST*:PASSED

If the test failed, the program will print *TEST*:FAILED (*REASON*)

If the test failed and did not return a log, the program will print *TEST*:FAILED (Unknown)

Credit for most of the code: https://www.tutorialspoint.com/How-can-I-get-the-list-of-files-in-a-directory-using-C-Cplusplus

*/


#include <iostream>
#include <fstream>
#include <sstream>
#include <dirent.h>
#include <sys/types.h>
#include <string.h>

using namespace std;
void test_files(const char *path) {
   struct dirent *entry;
   DIR *dir = opendir(path);
   
   if (dir == NULL) {
      return;
   }
   while ((entry = readdir(dir)) != NULL) {
        // get file type
        auto out = std::string(entry->d_name);
        int index  = out.find('.');

        //if file is test file, run it and get results
        if(index < 1000000 && out.substr(index+1) == "test" && out != "Test_All.test")
        {
            int index2 = out.find('_');

            // run test
            system(("./" + out + " > out.txt").c_str());

            // read result
            std::ifstream file("out.txt");
            std::string hold = "";
            file >> hold;
            file.close();

            // If file passed, print pass information (see description in the format)
            if(hold == "PASSED")
            {
               // Print passed
               std::cout<<out.substr(index2+1,index - index2-1)<<": PASSED"<<std::endl;

            }else{
               // If file failed, print failed information (see description in the format)

               try{
                  // try to get the reason of failure
                  std::ifstream file(out.substr(index2+1,index - index2-1) + "_LOG.txt");
                  std::stringstream buffer;
                  buffer << file.rdbuf();
                  file.close();

                  hold = buffer.str();
                  
               }catch(...)
               {
                  // if we can't get reason, just mark as unknown
                  hold = "Unknown";
               }

               // print out it failed and the reason if there is one
               std::cout<<out.substr(index2+1,index - index2-1)<<": FAILED ("<<hold<<")"<<std::endl;
            }



        }
   }
   closedir(dir);
}
int main() {
   test_files("./");

   // clear test files
   system("rm -r *");
}

