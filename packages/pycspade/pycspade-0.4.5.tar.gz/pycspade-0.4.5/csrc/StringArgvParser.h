#ifndef SPADE_UTILITY_STRINGARGVPARSER_H
#define SPADE_UTILITY_STRINGARGVPARSER_H

#include <iostream>
#include <string>

/**
 * Same as strdup. Make a deep copy of a string
 * @param s
 * @return
 */
char *copyChars(const char *s);

/**
 * Tuple containing argc and argv (char**)
 */
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

/**
 * Parse a string of arguments into char** (such that can be used by main())
 * This function is string aware, e.g. "hello world" is one arg, not two
 * @param s
 * @return 
 */
args_t* parse(const std::string& s);

#endif //SPADE_UTILITY_STRINGARGVPARSER_H
