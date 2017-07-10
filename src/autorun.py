#! /usr/bin/python3

import os
import sys

path = '../data/uuf50-218/UUF50.218.1000/'
#path = '../data/uf20-91/'
os.system('ls %s > list.txt' % path)
f = open('list.txt', 'r')
for x in f.readlines():
    tpath = 'python3 solver.py ' + path + x
    os.system(tpath)
    #break
f.close()
