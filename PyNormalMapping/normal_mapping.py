"""Usage: slice_map_generator.py [--d=<ID>]

Options:
    -h --help Show this screen.
    --d=<ID>  Volume ID [default: 16944]
"""
#!/usr/bin/python2

# import os
from docopt import docopt
# from PIL import Image
import timeit
from math import floor
import struct

WIDTH = 256
HEIGHT = 256
DEPTH = 256

def run(_id):
    data_file = open("eucrib256.raw", "rb")
    data_arr = []
    loaded = 0
    size = 500
    try:
        # data_arr = struct.unpack('i', data_file.read(int(round(WIDTH*HEIGHT*DEPTH))))

        # byte = struct.unpack('i', data_file.read(1))
        byte = data_file.read(1)
        while byte != "":
            # data_arr.append(byte)
            data_arr.append(ord(byte))
            byte = data_file.read(1)

            loaded += 1
            print("Loaded: " + str(round((loaded*100)/(WIDTH*HEIGHT*DEPTH), 2)) + "", end="\r")
            if loaded == size*5000:
                print("Loaded: " + str(round((loaded*100)/(WIDTH*HEIGHT*DEPTH), 2)) + "")
                print(len(data_arr))
                break
    finally:
        data_file.close()

    normal_arr = [None]*size

    # for i in range(0, data_file.length):
    for i in range(0, size):
        at = [None]*3
        at[0] = float(i % DEPTH)
        at[1] = float((i / DEPTH) % HEIGHT)
        at[2] = float(i / (HEIGHT * DEPTH))
        # at = [i % DEPTH, (i / DEPTH) % HEIGHT, i / (HEIGHT * DEPTH)]
        normal_arr[i] = getNormal(data_arr, at)
        print(at)
        # print(getNormal(data_arr, [i % DEPTH, (i / DEPTH) % HEIGHT, i / (HEIGHT * DEPTH)]))

    # normal_map = open('normal_map.raw', 'wb')
    # normal_map.write(bytearray(normal_arr))


def getNormal(data_arr, at):
    texpos1 = [None]*3

    w1 = at[2] - floor(at[2])
    w0 = (at[2] - (1.0/DEPTH)) - floor(at[2])
    w2 = (at[2] + (1.0/DEPTH)) - floor(at[2])

    # float fx, fy, fz;

    # float L0, L1, L2, L3, L4, L5, L6, L7, L8;
    # float H0, H1, H2, H3, H4, H5, H6, H7, H8;

    texpos1[2] = at[2] - 1.0/DEPTH
    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    L0 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    L1 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    L2 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    L3 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    L4 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    L5 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    L6 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    L7 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    L8 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0


    texpos1[2] = at[2] + 1.0/DEPTH
    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    # print("H0: " + str(int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))))
    H0 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    H1 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] + 1.0/HEIGHT
    H2 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    H3 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    H4 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] + 0.0/HEIGHT
    H5 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] - 1.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    H6 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 0.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    H7 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    texpos1[0] = at[0] + 1.0/WIDTH
    texpos1[1] = at[1] - 1.0/HEIGHT
    H8 = data_arr[int(round(DEPTH*HEIGHT*texpos1[2]+HEIGHT*texpos1[1]+texpos1[0]))]/255.0

    # we need to get interpolation of 2 x points
    # x direction
    # -1 -3 -1   0  0  0   1  3  1
    # -3 -6 -3   0  0  0   3  6  3
    # -1 -3 -1   0  0  0   1  3  1
    # y direction
    #  1  3  1   3  6  3   1  3  1
    #  0  0  0   0  0  0   0  0  0
    # -1 -3 -1  -3 -6 -3  -1 -3 -1
    # z direction
    # -1  0  1   -3  0  3   -1  0  1
    # -3  0  3   -6  0  6   -3  0  3
    # -1  0  1   -3  0  3   -1  0  1

    fx =  ((w0 * (H0 - L0)) + L0) * -1.0
    fx += ((w1 * (H0 - L0)) + L0) * -3.0
    fx += ((w2 * (H0 - L0)) + L0) * -1.0

    fx += ((w0 * (H3 - L3)) + L3) * -3.0
    fx += ((w1 * (H3 - L3)) + L3) * -6.0
    fx += ((w2 * (H3 - L3)) + L3) * -3.0

    fx += ((w0 * (H6 - L6)) + L6) * -1.0
    fx += ((w1 * (H6 - L6)) + L6) * -3.0
    fx += ((w2 * (H6 - L6)) + L6) * -1.0

    fx += ((w0 * (H1 - L1)) + L1) * 0.0
    fx += ((w1 * (H1 - L1)) + L1) * 0.0
    fx += ((w2 * (H1 - L1)) + L1) * 0.0

    fx += ((w0 * (H4 - L4)) + L4) * 0.0
    fx += ((w1 * (H4 - L4)) + L4) * 0.0
    fx += ((w2 * (H4 - L4)) + L4) * 0.0

    fx += ((w0 * (H7 - L7)) + L7) * 0.0
    fx += ((w1 * (H7 - L7)) + L7) * 0.0
    fx += ((w2 * (H7 - L7)) + L7) * 0.0

    fx += ((w0 * (H2 - L2)) + L2) * 1.0
    fx += ((w1 * (H2 - L2)) + L2) * 3.0
    fx += ((w2 * (H2 - L2)) + L2) * 1.0

    fx += ((w0 * (H5 - L5)) + L5) * 3.0
    fx += ((w1 * (H5 - L5)) + L5) * 6.0
    fx += ((w2 * (H5 - L5)) + L5) * 3.0

    fx += ((w0 * (H8 - L8)) + L8) * 1.0
    fx += ((w1 * (H8 - L8)) + L8) * 3.0
    fx += ((w2 * (H8 - L8)) + L8) * 1.0

    fy =  ((w0 * (H0 - L0)) + L0) * 1.0
    fy += ((w1 * (H0 - L0)) + L0) * 3.0
    fy += ((w2 * (H0 - L0)) + L0) * 1.0

    fy += ((w0 * (H3 - L3)) + L3) * 0.0
    fy += ((w1 * (H3 - L3)) + L3) * 0.0
    fy += ((w2 * (H3 - L3)) + L3) * 0.0

    fy += ((w0 * (H6 - L6)) + L6) * -1.0
    fy += ((w1 * (H6 - L6)) + L6) * -3.0
    fy += ((w2 * (H6 - L6)) + L6) * -1.0

    fy += ((w0 * (H1 - L1)) + L1) * 3.0
    fy += ((w1 * (H1 - L1)) + L1) * 6.0
    fy += ((w2 * (H1 - L1)) + L1) * 3.0

    fy += ((w0 * (H4 - L4)) + L4) * 0.0
    fy += ((w1 * (H4 - L4)) + L4) * 0.0
    fy += ((w2 * (H4 - L4)) + L4) * 0.0

    fy += ((w0 * (H7 - L7)) + L7) * -3.0
    fy += ((w1 * (H7 - L7)) + L7) * -6.0
    fy += ((w2 * (H7 - L7)) + L7) * -3.0

    fy += ((w0 * (H2 - L2)) + L2) * 1.0
    fy += ((w1 * (H2 - L2)) + L2) * 3.0
    fy += ((w2 * (H2 - L2)) + L2) * 1.0

    fy += ((w0 * (H5 - L5)) + L5) * 0.0
    fy += ((w1 * (H5 - L5)) + L5) * 0.0
    fy += ((w2 * (H5 - L5)) + L5) * 0.0

    fy += ((w0 * (H8 - L8)) + L8) * -1.0
    fy += ((w1 * (H8 - L8)) + L8) * -3.0
    fy += ((w2 * (H8 - L8)) + L8) * -1.0


    fz =  ((w0 * (H0 - L0)) + L0) * -1.0
    fz += ((w1 * (H0 - L0)) + L0) * 0.0
    fz += ((w2 * (H0 - L0)) + L0) * 1.0

    fz += ((w0 * (H3 - L3)) + L3) * -3.0
    fz += ((w1 * (H3 - L3)) + L3) * 0.0
    fz += ((w2 * (H3 - L3)) + L3) * 3.0

    fz += ((w0 * (H6 - L6)) + L6) * -1.0
    fz += ((w1 * (H6 - L6)) + L6) * 0.0
    fz += ((w2 * (H6 - L6)) + L6) * 1.0

    fz += ((w0 * (H1 - L1)) + L1) * -3.0
    fz += ((w1 * (H1 - L1)) + L1) * 0.0
    fz += ((w2 * (H1 - L1)) + L1) * 3.0

    fz += ((w0 * (H4 - L4)) + L4) * -6.0
    fz += ((w1 * (H4 - L4)) + L4) * 0.0
    fz += ((w2 * (H4 - L4)) + L4) * 6.0

    fz += ((w0 * (H7 - L7)) + L7) * -3.0
    fz += ((w1 * (H7 - L7)) + L7) * 0.0
    fz += ((w2 * (H7 - L7)) + L7) * 3.0

    fz += ((w0 * (H2 - L2)) + L2) * -1.0
    fz += ((w1 * (H2 - L2)) + L2) * 0.0
    fz += ((w2 * (H2 - L2)) + L2) * 1.0

    fz += ((w0 * (H5 - L5)) + L5) * -3.0
    fz += ((w1 * (H5 - L5)) + L5) * 0.0
    fz += ((w2 * (H5 - L5)) + L5) * 3.0

    fz += ((w0 * (H8 - L8)) + L8) * -1.0
    fz += ((w1 * (H8 - L8)) + L8) * 0.0
    fz += ((w2 * (H8 - L8)) + L8) * 1.0
    return [fx/27.0 , fy/27.0 , fz/27.0]


if __name__ == "__main__":
    arguments = docopt(__doc__, version="reactor 0.1")
    _id = arguments["--d"]

    t = timeit.Timer(lambda: run(_id))
    print("Total time: " + str(t.timeit(number=1)))
