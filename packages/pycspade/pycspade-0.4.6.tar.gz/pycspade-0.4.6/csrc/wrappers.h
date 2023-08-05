//
// Created by Yukio Fukuzawa on 3/12/18.
//

#ifndef SPADE_UTILITY_WRAPPERS_H
#define SPADE_UTILITY_WRAPPERS_H

#include <iostream>
#include "utils.h"


/**
 * Call makebin given the argument list as std::string
 * @param args e.g 'makebin test/zaki.txt zaki.data'
 */
void makebinWrapper(const std::string& args);

/**
 * Call getconf given the argument list as std::string
 * @param args e.g. 'getconf -i zaki -o zaki'
 */
void getconfWrapper(const std::string& args);

/**
 * Call exttpose given the argument list as std::string
 * @param args e.g. 'exttpose -i zaki -o zaki -p 1 -l -x -s 0.3'
 */
void exttposeWrapper(const std::string& args);

/**
 * Call spade given the argument list as std::string
 * @param args e.g 'spade -i zaki -s 0.3 -Z 10 -z 10 -u 1 -r -e 1 -o'
 */
void spadeWrapper(const std::string& args);

/**
 * After calling all 4 functions, the result will be made available as several streams of text
 * Call this function to get those streams and reset them to empty.
 * Don't call this twice. The second time it is called all the streams will be empty
 * @return
 */
result_t getResult();

/**
 * One function to call all 4 functions and return the result
 * @param filename name of the input file, e.g. /path/to/zaki.txt
 * @param args arguments to spade.
 * @param tmpdir temporary folder for spade to operate. Temp files will be cleaned afterwards. Must end with a slash
 * @return same as getResult
 */
result_t runSpade(const std::string& filename, spade_arg_t args, const std::string& tmpdir = "/tmp/");

#endif //SPADE_UTILITY_WRAPPERS_H
