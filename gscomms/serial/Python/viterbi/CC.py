import numpy as np


def CC(bits):
    '''
    Take in 3 bits in as numpy array and convert to CC

    Param:
        bits - 3 bits in a numpy array
    Returns:
        return 3 bits
    '''

    # Pre-declare an empty array of zeros
    cc = np.zeros(3)

    # Convert 3 bits to cc repersentation
    cc[0] = bits.sum() % 2
    cc[1] = (bits[1] + bits[2]) % 2
    cc[2] = (bits[0] + bits[2]) % 2

    # Return CC
    return cc

def CC_Array(bits):
    '''
    Take in bits in as numpy array and convert to CC

    Param:
        bits - bits in a numpy array
    Returns:
        return CC bits
    '''
    # Empty array to return later
    new_bits = np.empty(0)

    for x in range(bits.size-3,-1,-1):
        new_bits = np.append(new_bits,CC(bits[x:x+3]))

    return new_bits.astype(int).astype(str)
