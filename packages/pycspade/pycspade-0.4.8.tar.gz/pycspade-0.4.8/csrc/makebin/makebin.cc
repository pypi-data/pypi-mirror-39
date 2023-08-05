#include <cerrno>
#include <iostream>
#include <cstdio>
#include <fstream>
#include <strstream>
#include <cstdlib>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <cmath>
#include <cstring>
#include "../funcs.h"


namespace utility {
    namespace makebin {

#define ITSZ sizeof(int)
        const int lineSize = 8192;
        const int wdSize = 256;
        std::ifstream fin;
        std::ofstream fout;

        void convbin(char *inBuf, int inSize) {
            char inStr[wdSize];
            std::istrstream ist(inBuf, inSize);
            int it;
            while (ist >> inStr && strlen(inStr)) {
                it = atoi(inStr);
                //std::cout << it  << " ";
                fout.write((char *) &it, ITSZ);
                //std::cout << it << " ";
            }
        }

        void makebinFunc(int argc, char **argv) {
            char inBuf[lineSize];
            int inSize;
            fin.open(argv[1]);
            fout.open(argv[2]);

            if (!fin) {
                std::string error_message = "can't open ascii file: " + std::string(argv[1]);
                throw std::runtime_error(error_message);
            }
            if (!fout) {
                std::string error_message = "can't open binary file: " + std::string(argv[2]);
                throw std::runtime_error(error_message);
            }

            while (fin.getline(inBuf, lineSize)) {
                inSize = fin.gcount();
                //std::cout << "IN SIZE " << inSize << std::endl;
                convbin(inBuf, inSize);
            }
            std::flush(std::cout);
            fout.close();
            fin.close();
        }
    }
}

void makebinFunc(int argc, char **argv) {
    utility::makebin::makebinFunc(argc, argv);
}
