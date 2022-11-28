import numpy as np
import viterbi

def CC_to_Bin(bits):
    '''
    Take in a 3 bit CC and return binary repsentation

    Param:
        bits - 3 bit CC
    Returns:
        3 binary bits
    '''

    if (bits == np.array([0,0,0])).all():
        return np.array([0,0,0])
    elif (bits == np.array([1,1,1])).all():
        return np.array([0,0,1])
    elif (bits == np.array([1,1,0])).all():
        return np.array([0,1,0])
    elif (bits == np.array([1,0,1])).all():
        return np.array([1,0,0])
    elif (bits == np.array([1,0,0])).all():
        return np.array([1,1,1])
    elif (bits == np.array([0,1,1])).all():
        return np.array([1,1,0])
    elif (bits == np.array([0,0,1])).all():
        return np.array([0,1,1])
    else:
        return np.array([1,0,1])

def Decode(data):
    '''
    Take in a string binary that has undergone CC and convert it back to binary

    Param:
        data - binary string after CC
    Returns:
        binary string
    '''

    # Convert to numpy array
    bin = np.array(list(data)).astype(int)

    # If a blank string was passed, end function
    if bin.size == 0:
        return ''

    # correct errors
    bin = viterbi.Viterbi(bin)

    # In the event we were unable to correct any errors return a blank string
    if bin.size == 0:
        return ''

    hold = CC_to_Bin(bin[-3:]).astype(str)

    for x in range(len(data)-6,-1,-3):
        hold = np.append(hold, (CC_to_Bin(bin[x:x+3]).astype(str))[2])

    # Rejoin as a binary string
    return ''.join(hold.tolist())
