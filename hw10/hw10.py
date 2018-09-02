# This block checks for proper cython setup arguments
# you can provide your own if you want to test out different
# options and this block will be mainly ignored
import sys
print("==================================================")
if len(sys.argv) == 1: # no command line args
    print("*hw10.py Running with setup with default args")
    print("\t adding \"build_ext\" and \"--inplace\" to sys.argv")
    sys.argv = ["hw10.py", "build_ext", "--inplace"]


# This block compiles/sets up the hw10 module
# from the  hw10.pyx cython file
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("hw10.pyx"))
print("*hw10.py Setup complete!")
print("==================================================\n")


# This is where I import the pre-compiled 
# module and enter the Cython layer
import hw10
if __name__ == "__main__":
    hw10.main()
