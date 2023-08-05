import pandas as pd

def wavelength_between(spectrum, left, right, inclusive=True):
    flags = spectrum['wavelength'].between(left, right, inclusive=inclusive)
    i_flags = flags.index[flags]
    return spectrum.loc[i_flags[0]:i_flags[-1]+1]