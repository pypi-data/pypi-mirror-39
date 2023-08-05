from io import StringIO
import logging

import numpy as np
import pandas as pd
import xarray as xr

logger = logging.getLogger()

def read_sections(lines, section):
    for i, line in enumerate(lines):
        if line.startswith(section):
            # line information locates at the last column
            n_line = int(line.split()[-1])
            logger.debug("\"{}\" contains {} rows".format(section, n_line))
            return lines[i+1:(i+1)+n_line]
    raise ValueError("unable to locate \"{}\"".format(section))

def open_thermo(path, parse_name=False):
    """Open data file from Thermo

    Returns
    -------
    data : pd.DataFrame
        Measured spectrum stored in the file.
    """
    with open(path, 'r') as fd:
        # NOTE
        # load all the file in-memory, assuming small data size
        lines = fd.read().split('\n')

    if parse_name:
        name = read_sections(lines, 'finalresult')
        if len(name) > 1:
            name = None
            logger.info("mixture spectrum")
        else:
            name = name[0].split()[1].lower()
            logger.info("spectra of \"{}\"".format(name))

    s_data = read_sections(lines, 'spectrum')
    _s_data = StringIO('\n'.join(s_data))
    i_data = pd.read_csv(
        _s_data, 
        sep=' ', 
        header=None, 
        names=['wavelength', 'intensity'], 
        dtype=np.float32
    )

    if parse_name:
        return name, i_data
    else:
        return i_data