from setuptools import setup, Extension
from codecs import open

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

if use_cython:
    sourcefiles = ['pycspade/cspade.pyx']
else:
    sourcefiles = ['pycspade/cspade.cpp']

extra_files = ['csrc/{}'.format(x) for x in [
    'StringArgvParser.cc',
    'exttpose/Array.cc',
    'spade/ArraySpade.cc',
    'spade/Database.cc',
    'spade/Eqclass.cc',
    'spade/extl2.cc',
    'spade/HashTable.cc',
    'spade/Itemset.cc',
    'spade/Lists.cc',
    'spade/maxgap.cc',
    'spade/partition.cc',
    'spade/sequence.cc',
    'exttpose/exttpose.cc',
    'makebin/makebin.cc',
    'getconf/getconf.cc',
    'getconf/calcdb.cc',
    'exttpose/calcdb.cc',
    'wrappers.cc',
    'utils.cc'
]]

ext_modules = [
    Extension('pycspade.cspade',
              sourcefiles + extra_files,
              include_dirs=['csrc/'],
              language='c++',
              extra_compile_args=[
                  '-std=c++11',
                  '-Wno-sign-compare',
                  '-Wno-incompatible-pointer-types',
                  '-Wno-unused-variable',
                  '-Wno-absolute-value',
                  '-Wno-visibility',
                  '-Wno-#warnings']
              ),
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pycspade',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    license='MIT',
    packages=['pycspade'],
    version='0.4.1',
    author=['Mohammed J. Zaki', 'Yukio Fukuzawa'],
    description='C-SPADE Python Implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fzyukio/python-cspade',
    keywords=['cspade', 'c-spade', 'sequence mining'],
    install_requires=['Cython'],

)
