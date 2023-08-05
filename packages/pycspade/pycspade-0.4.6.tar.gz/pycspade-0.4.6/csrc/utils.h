#ifndef UTILS_H
#define UTILS_H

#include <algorithm>
#include <sstream>
#include <fstream>
#include <list>

using std::ostringstream;
using std::string;
using std::ifstream;
using std::list;

#ifndef bzero
#define bzero(b, len) (memset((b), '\0', (len)), (void) 0)
#endif

const char alphanum[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const int alphanumlen = sizeof(alphanum) - 1;

// Logger and mem logger
extern std::ostringstream logger;
extern std::ostringstream mined;
extern std::ostringstream memlog;

struct result_t {
    int nsequences;
    std::string mined;
    std::string logger;
    std::string memlog;
};

struct spade_arg_t {
    double support = 0.1;
    int maxsize = -1;
    int maxlen = -1;
    int mingap = -1;
    int maxgap = -1;
    int memsize = -1;
    int numpart = -1;
    int maxwin = -1;
    bool bfstype = false;
    bool tid_lists = false;
};


bool file_exists(const std::string &name);

int num_lines(const std::string &filename);

std::list<std::string> list_files(const std::string& folder, const std::string& prefix = "");

std::string random_id(const int len);

#endif
