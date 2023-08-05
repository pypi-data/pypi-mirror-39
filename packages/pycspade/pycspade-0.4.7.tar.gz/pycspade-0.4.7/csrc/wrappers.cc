#include <cmath>
#include "StringArgvParser.h"
#include "wrappers.h"
#include "funcs.h"
#include "spade/spade.h"

void spadeWrapper(const std::string &args) {
    args_t *arguments = parse(args);
    sequenceFunc(arguments->argc, arguments->argv);
    delete arguments;
}

void exttposeWrapper(const std::string &args) {
    args_t *arguments = parse(args);
    exttposeFunc(arguments->argc, arguments->argv);
    delete arguments;
}

void getconfWrapper(const std::string &args) {
    args_t *arguments = parse(args);
    getconfFunc(arguments->argc, arguments->argv);
    delete arguments;
}

void makebinWrapper(const std::string &args) {
    args_t *arguments = parse(args);
    makebinFunc(arguments->argc, arguments->argv);
    delete arguments;
}

result_t getResult() {
    result_t result;

    result.mined = mined.str();
    result.logger = logger.str();
    result.memlog = memlog.str();
    result.nsequences = DBASE_NUM_TRANS;

    // Clear the std::stringstream otherwise the next run will get duplicated result
    mined.str(std::string());
    mined.clear();
    logger.str(std::string());
    logger.clear();
    memlog.str(std::string());
    memlog.clear();
    return result;
}

void clean_up(const std::string& tmpprefix) {
    std::list<std::string> tmpfiles = list_files("/tmp", tmpprefix);
    for (std::string& tmpfile : tmpfiles) {
        std::string filepath = "/tmp/" + tmpfile;
        if(remove(filepath.c_str()) != 0) {
            logger << "Error deleting file " << filepath << std::endl;
        }
        else {
            logger << "Cleaned up successful: " << filepath << std::endl;
        }
    }
}

result_t runSpade(const std::string &filename, spade_arg_t args, const std::string& tmpdir) {

    if (!file_exists(filename)) {
        throw std::runtime_error("File " + filename + " does not exist.");
    }

    if (args.support <= 0 || args.support > 1) {
        throw std::runtime_error("Support must be a floating point in range (0-1]");
    }

    if (args.mingap > 0 && args.maxgap > 0 && args.maxgap < args.mingap) {
        args.mingap = args.maxgap;
    }

    int nrows = num_lines(filename);
    std::stringstream opt;

    auto nop = static_cast<int>(ceil((nrows + 2 * nrows) * sizeof(long) / pow(4, 10) / 5));
    if (args.memsize > 0) {
        opt << "-m " << args.memsize;
        nop = static_cast<int>(ceil(nop * 32 / args.memsize));
    }

    if (args.numpart > 0) {
        if (args.numpart < nop) {
            logger << "numpart less than recommended\n";
        }
        nop = args.numpart;
    }

    std::string random_suffix = random_id(16);
    std::string tmpprefix = "cspade-" + random_suffix;
    std::string otherfile = tmpdir + tmpprefix;
    std::string datafile = otherfile + ".data";

    std::stringstream makebin_args;
    std::stringstream getconf_args;
    std::stringstream exttpose_args;
    std::stringstream spade_args;

    makebin_args << "makebin " << filename << " " << datafile;
    getconf_args << "getconf -i " << otherfile << " -o " << otherfile;
    exttpose_args << "exttpose -i " << otherfile << " -o " << otherfile << " -p " << nop << " -l -x -s " << args.support;

    if (args.maxsize > 0) {
        opt << " -Z " << args.maxsize;
    }
    if (args.maxlen > 0) {
        opt << " -z " << args.maxlen;
    }
    if (args.mingap > 0) {
        opt << " -l " << args.mingap;
    }
    if (args.maxgap > 0) {
        opt << " -u " << args.maxgap;
    }
    if (args.maxwin > 0) {
        opt << " -w " << args.maxwin;
    }
    if (not args.bfstype) {
        opt << " -r";
    }
    if (args.tid_lists) {
        opt << " -y";
    }

    spade_args << "spade -i " << otherfile << " -s " << args.support << opt.str() << " -e " << nop << " -o";

    try {
        makebinWrapper(makebin_args.str());
        getconfWrapper(getconf_args.str());
        exttposeWrapper(exttpose_args.str());
        spadeWrapper(spade_args.str());

        clean_up(tmpprefix);
        return getResult();
    }
    catch (std::runtime_error& e) {
        clean_up(tmpprefix);
        throw e;
    }
    catch (std::exception& e) {
        clean_up(tmpprefix);
        throw e;
    }
}
