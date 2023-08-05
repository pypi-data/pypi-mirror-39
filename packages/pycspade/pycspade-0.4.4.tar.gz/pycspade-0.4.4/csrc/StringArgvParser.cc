//
// Created by Yukio Fukuzawa on 2/12/18.
//

#include <err.h>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <string>
#include <list>
#include <sstream>

#include "utils.h"
#include "StringArgvParser.h"


char *copyChars(const char *s) {
    char *d = static_cast<char *>(malloc(strlen(s) + 1));
    if (d == NULL) return NULL;
    strcpy(d, s);
    return d;
}

std::string ensure_one_newline(const std::string& s) {
    std::string str(s);
    str.erase(std::remove(str.begin(), str.end(), '\n'), str.end());
    return str + "\n";
}

args_t* parse(const std::string& s) {
    int argc = 0;
    std::list<std::string> argv;
    std::stringstream token;

    bool in_token;
    bool in_container;
    bool escaped;
    char container_start;
    char c;
    int len;
    int i;

    std::string str = ensure_one_newline(s);

    container_start = 0;
    in_token = false;
    in_container = false;
    escaped = false;

    len = static_cast<int>(str.length());

    for (i = 0; i < len; i++) {
        c = str[i];

        switch (c) {
            /* handle whitespace */
            case ' ':
            case '\t':
            case '\n':
                if (!in_token)
                    continue;

                if (in_container) {
                    token << c;
                    continue;
                }

                if (escaped) {
                    escaped = false;
                    token << c;
                    continue;
                }

                /* if reached here, we're at end of token */
                in_token = false;
                argv.push_back(token.str());
                argc++;
                token.str(std::string());
                token.clear();
                break;

                /* handle quotes */
            case '\'':
            case '\"':

                if (escaped) {
                    token << c;
                    escaped = false;
                    continue;
                }

                if (!in_token) {
                    in_token = true;
                    in_container = true;
                    container_start = c;
                    continue;
                }

                if (in_container) {
                    if (c == container_start) {
                        in_container = false;
                        in_token = false;
                        argv.push_back(token.str());
                        argc++;
                        token.str(std::string());
                        token.clear();
                        continue;
                    } else {
                        token << c;
                        continue;
                    }
                }

                /* XXX in this case, we:
                 *    1. have a quote
                 *    2. are in a token
                 *    3. and not in a container
                 * e.g.
                 *    hell"o
                 *
                 * what'str done here appears shell-dependent,
                 * but overall, it'str an error.... i *think*
                 */
                throw std::runtime_error("Parse Error! Bad quotes");
            case '\\':

                if (in_container && str[i + 1] != container_start) {
                    token << c;
                    continue;
                }

                if (escaped) {
                    token << c;
                    continue;
                }

                escaped = true;
                break;

            default:
                if (!in_token) {
                    in_token = true;
                }

                token << c;
        }
    }

    if (in_container)
        throw std::runtime_error("Parse Error! Still in container\n");

    if (escaped)
        throw std::runtime_error("Parse Error! Unused escape (\\)\n");
    
    auto * retval = new args_t();

//    std::list<std::string>& argv = parser.getArgv();
//    int argc = parser.getArgc();

    auto ** argv_char = new char*[argc]();

    std::list<std::string>::const_iterator iterator;
    int idx = 0;
    for (iterator = argv.begin(); iterator != argv.end(); ++iterator) {
        const char* arg = (*iterator).c_str();
        argv_char[idx] = copyChars(arg);
        idx++;
    }

    retval->argc = argc;
    retval->argv = argv_char;
    return retval;
}
