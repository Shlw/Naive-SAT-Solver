#! /usr/bin/python3

import os
import sys

path = '../data/uf100-430/'
path = '../data/uf20-91/'
path = '../data/uuf50-218/UUF50.218.1000/'
path = '../data/uuf100-430/UUF100.430.1000/'
os.system('ls %s > list.txt' % path)
f = open('list.txt', 'r')
cnt = 0
for x in f.readlines():
    tpath = 'python3 main.py ' + path + x
    print(cnt)
    os.system(tpath)
    cnt += 1
    #if cnt > 10:
        #break
f.close()
