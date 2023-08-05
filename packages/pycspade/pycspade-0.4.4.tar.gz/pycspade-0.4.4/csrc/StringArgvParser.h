#ifndef SPADE_UTILITY_STRINGARGVPARSER_H
#define SPADE_UTILITY_STRINGARGVPARSER_H

#include <iostream>
#include <string>

char *copyChars(const char *s);

struct args_t {
    int argc;
    char **argv;

    ~args_t() {
        for (int i=0; i<argc; i++) {
            delete [] argv[i];
        }
        delete [] argv;
    }
};

args_t* parse(const std::string& s);

#endif //SPADE_UTILITY_STRINGARGVPARSER_H
