# don't import h5py and mpi4py in a Pythran file, here, no problem!
import h5py
import mpi4py

from fluidpythran import pythran_def

@pythran_def
def myfunc(a: int, b: float):
    return a * b