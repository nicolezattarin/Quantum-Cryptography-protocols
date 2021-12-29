import numpy as np
import pandas as pd
from bitarray import bitarray

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", default='QKD_Lab_data/input-keys.bob', help="filename.", type=str)
parser.add_argument("--maxiter", default=None, help="maximum keys to read.", type=int)

def main(filename, maxiter):
    """
    Read the data from the filename file given as argument and decode the keys encoded.

    Each file contains key blocks of different lengths. A file begins with 8 bytes that code for 
    a uint64 big-endian, which is the length N of the block (in bytes). 
    After these first 8 bytes, N bytes (=8N bits) of raw keys follow.
    After the N bytes, another block begins.

    Each QKD state is represented by two bits.
    Encoding of input-keys.alice: (00,H), (01,V), (10,D), (11,A) A not used in the three state protocol.
    Encoding of input-keys.decoy: (00,Strong Intensity), (01,Low Intensity), (10,unused), (11,unused).
    Encoding of input-keys.bob: (00,H), (01,V), (10,D), (11,A).
    
    This code saves the decoded keys in a .csv file with the corresponding block length.

    args:
        filename: path to the file to read.
        maxiter: maximum number of keys to read.
    """
    keys = []
    block_sizes = []

    #decode file
    bytes = np.fromfile(filename, dtype = "uint8")
    i=0
    while i<len(bytes):
        block_size = int.from_bytes(bytes[i:i+8], byteorder='big')
        i += 8
        b = bytes[i:i+block_size]
        key = np.unpackbits(b, bitorder='little')
        i+=block_size
        keys.append(key)
        block_sizes.append(block_size)
    
    #decode keys
    decoded_keys = []
    count = 0
    for k in keys:
        print("Decoding key: ", count, " of ", len(keys))
        decoded = []
        k = np.split(k, len(k)//2)
        if filename[:5] != 'alice' or filename[:3] == 'bob':
            for pair in k:
                if (pair==[0,0]).all(): decoded.append('H')
                elif (pair==[0,1]).all(): decoded.append('V')
                elif (pair==[1,0]).all(): decoded.append('D')
                elif (pair==[1,1]).all(): decoded.append('A')
            decoded_keys.append(decoded)
            if maxiter != None and count == maxiter-1: break
            count+=1
        else:
            for pair in k:
                if (pair==[0,0]).all(): decoded.append('S')
                elif (pair==[0,1]).all(): decoded.append('L')
                elif (pair==[1,0]).all(): decoded.append('Unused')
                elif (pair==[1,1]).all(): decoded.append('Unused')
            decoded_keys.append(decoded)
            if maxiter != None and count == maxiter-1: break
            count+=1

    decoded_keys = np.array(decoded_keys)
    block_sizes = np.array(block_sizes)

    print(decoded_keys.shape, block_sizes.shape)

    #check if keys are correct
    print ("Decoded key (first 3 bytes): ", decoded_keys[0][:12])

    #save to csv
    import os
    dir = 'QKD_keys'
    if os.path.isdir(dir)==False:
        os.mkdir(dir)

    df = pd.DataFrame(decoded_keys, columns=['key'])
    df['block_size'] = block_sizes
    if filename[:5] != 'alice':
        df.to_csv(dir+'/decoded_keys_alice.csv', index=False)
    elif filename[:3] == 'bob':
        df.to_csv(dir+'/decoded_keys_bob.csv', index=False)
    elif filename[:5] == 'decoy':
        df.to_csv(dir+'/decoded_keys_decoy.csv', index=False)

    print("Done!")

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)