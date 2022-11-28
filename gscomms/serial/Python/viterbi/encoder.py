import numpy as np
from viterbi import CC_Array


def Encode(data):
    '''
    Take in binary string and encode to CC

    Param:
        data - binary string
    Returns:
        returns binary string with CC
    '''

    # Convert to numy array
    bin = np.array(list(data)).astype(int)

    # Convert bin to CC array
    CC_arr = CC_Array(bin)

    # Convert CC Array to binary string
    return ''.join(CC_arr.tolist())
