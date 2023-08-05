from libcpp cimport bool
from libcpp.string cimport string as c_string

cdef extern from "../csrc/utils.h":
    cdef struct result_t:
        int nsequences;
        c_string mined;
        c_string logger;
        c_string memlog;

    cdef struct spade_arg_t:
        double support;
        int maxsize;
        int maxlen;
        int mingap;
        int maxgap;
        int memsize;
        int numpart;
        int maxwin;
        bool bfstype;
        bool tid_lists;

cdef extern from "../csrc/wrappers.h":
    cdef void spadeWrapper(const c_string& args) except +RuntimeError;
    cdef void exttposeWrapper(const c_string& s) except +RuntimeError;
    cdef void getconfWrapper(const c_string& s) except +RuntimeError;
    cdef void makebinWrapper(const c_string& s) except +RuntimeError;
    cdef result_t getResult() except +RuntimeError;
    cdef result_t runSpade(const c_string& filename, spade_arg_t args) except +RuntimeError;


def c_makebin(args):
    args = 'makebin {} \n'.format(args)
    args = bytes(args, encoding='latin-1')
    return makebinWrapper(args)


def c_getconf(args):
    args = 'getconf {} \n'.format(args)
    args = bytes(args, encoding='latin-1')
    return getconfWrapper(args)


def c_exttpose(args):
    args = 'exttpose {} \n'.format(args)
    args = bytes(args, encoding='latin-1')
    return exttposeWrapper(args)


def c_spade(args):
    args = 'spade {} \n'.format(args)
    args = bytes(args, encoding='latin-1')
    return spadeWrapper(args)


def c_runspade(filename, support=0.1, maxsize=None, maxlen=None, mingap=None, maxgap=None, memsize=None, numpart=None,
               maxwin=None, bfstype=None, tid_lists=None):
    cdef spade_arg_t args
    args.support = support
    args.maxsize = maxsize or -1
    args.maxlen = maxlen or -1
    args.mingap = mingap or -1
    args.maxgap = maxgap or -1
    args.memsize = memsize or -1
    args.numpart = numpart or -1
    args.maxwin = maxwin or -1
    args.bfstype = bfstype or False
    args.tid_lists = bfstype or False

    filename = bytes(filename, encoding='ascii')
    return runSpade(filename, args)


def c_get_result(decode=True):
    """
    :param decode: if True, the return strings will be decoded and line-separated, otherwise raw C++ strings
                   (python bytes) are returned
    """
    cdef result = getResult()
    if decode:
        decode_result(result)
    return result


def decode_result(result):
    result['mined'] = result['mined'].decode('latin-1').split('\n')
    result['logger'] = result['logger'].decode('latin-1').split('\n')
    result['memlog'] = result['memlog'].decode('latin-1').split('\n')
    return