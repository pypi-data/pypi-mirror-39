from io import StringIO
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger()

def read_sections(lines, section):
    for i, line in enumerate(lines):
        if line.startswith(section):
            # line information locates at the last column
            n_line = int(line.split()[-1])
            logger.debug("\"{}\" contains {} rows".format(section, n_line))
            return lines[i+1:(i+1)+n_line]
    raise ValueError("unable to locate \"{}\"".format(section))

def open_thermo(path):
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

    s_data = read_sections(lines, 'spectrum')
    _s_data = StringIO('\n'.join(s_data))
    i_data = pd.read_csv(
        _s_data, 
        sep=' ', 
        header=None, 
        names=['wavelength', 'intensity'], 
        dtype=np.float32
    )
    return i_data