#include <sstream>
#include <cstdio>
#include <dirent.h>
#include <sys/types.h>
#include <random>
#include <iostream>

#include "utils.h"

using std::ostringstream;

std::ostringstream logger;
std::ostringstream mined;
std::ostringstream memlog;

bool file_exists(const std::string &name) {
    std::ifstream f(name.c_str());
    return f.good();
}

/* Reads a file and returns the number of lines in this file. */
int num_lines(const std::string &filename){
    FILE * file = fopen(filename.c_str(), "r");
    int lines = 0;
    int c;
    int last = '\n';
    while (EOF != (c = fgetc(file))) {
        if (c == '\n' && last != '\n') {
            ++lines;
        }
        last = c;
    }
    fclose(file);
    return lines;
}


bool starts_with(const std::string &haystack, const std::string &needle) {
    return needle.length() <= haystack.length()
           && equal(needle.begin(), needle.end(), haystack.begin());
}


std::list<std::string> list_files(const std::string& folder, const std::string& prefix) {
    struct dirent *entry;
    std::list<std::string> retval;
    DIR *dir = opendir(folder.c_str());
    if (dir == nullptr) {
        return retval;
    }

    bool check_prefix = prefix.length() > 0;

    while ((entry = readdir(dir)) != nullptr) {
        std::string filename = entry->d_name;
        if (check_prefix && starts_with(filename, prefix)) {
            retval.push_back(filename);
        }
    }
    closedir(dir);

    return retval;
}


std::string random_id(const int len) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, alphanumlen - 1);

    auto *s = new char[len + 1];
    int rand_idx;
    for (int i = 0; i < len; ++i) {
        rand_idx = dis(gen);
        s[i] = alphanum[rand_idx];
    }
    s[len] = 0;
    std::string retval(s);
    delete[] s;
    return retval;
}
