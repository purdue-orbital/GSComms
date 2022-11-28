import numpy as np

def Possibilities(bits):
        '''
        Given 3 bits, return the 2 next 3 possible bits

        Param:
            bits - 1 CC
        Returns:
            Return[0] - Possibility 1
            Return[1] - Possibility 2
        '''
        if (bits == np.array([0,0,0])).all() or (bits == np.array([1,1,1])).all():
            return np.array([[0,0,0],[1,0,1]])
        elif (bits == np.array([1,1,0])).all() or (bits == np.array([0,0,1])).all():
            return np.array([[1,1,1],[0,1,0]])
        elif (bits == np.array([1,0,1])).all() or (bits == np.array([0,1,0])).all():
            return np.array([[1,1,0],[0,1,1]])
        else:
            return np.array([[0,0,1],[1,0,0]])



def Viterbi(bits,size=0,index=0,cost=0):
    '''
    Take in bits that have under gone CC and correct any errors

    Param:
        bits - CC bits
        cost - current amount of bits that had to be flipped
    Returns:
        return corrected CC bits
    '''
    if index == 0:
        size = bits.size-3

    if index * 3 == size:
        return bits

    # get base
    base = bits[:((index + 1) * 3)]
    end = bits[(index + 2) * 3:]

    # get possible next values
    possible = Possibilities(base[-3:])

    # put new data into d1
    d1 = np.concatenate((base,possible[0],end))
    d2 = np.concatenate((base,possible[1],end))

    # Branch out
    data1 = Viterbi(d1,size,index + 1,0)
    data2 = Viterbi(d2,size,index + 1,0)

    # if data2 is blank return data1
    if data2.size == 0:
        return data1

    # if data1 is blank return data2
    if data1.size == 0:
        return data2

    cost1 = np.abs(data1 - bits).sum()
    cost2 = np.abs(data2 - bits).sum()

    if cost1 >= 5:
        data1 = np.empty(0)

    if cost2 >= 5:
        data2 = np.empty(0)

    # return the one with the smallest error
    if cost1 > cost2:
        return data2
    else:
        return data1
