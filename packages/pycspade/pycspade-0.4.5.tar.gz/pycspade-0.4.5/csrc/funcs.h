#ifndef SPADE_UTILITY_FUNCS_H
#define SPADE_UTILITY_FUNCS_H

#include "utils.h"

/**
 * Calls makebin the same way the executable would be called
 * E.g. makebin test/zaki.txt zaki.data
 *
 * @param argc
 * @param argv
 */
void makebinFunc(int argc, char **argv);

/**
 * Calls getconf the same way the executable would be called
 * E.g. getconf -i zaki -o zaki
 *
 * @param argc
 * @param argv
 */
void getconfFunc(int argc, char **argv);

/**
 * Calls exttpose the same way the executable would be called
 * E.g. exttpose -i zaki -o zaki -p 1 -l -x -s 0.3
 * @param argc
 * @param argv
 */
void exttposeFunc(int argc, char **argv);

/**
 * Calls sequence (spade) the same way the executable would be called
 * E.g. spade -i zaki -s 0.3 -Z 10 -z 10 -u 1 -r -e 1 -o
 * @param argc
 * @param argv
 */
void sequenceFunc(int argc, char **argv);

#endif //SPADE_UTILITY_FUNCS_H
