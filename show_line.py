#! /usr/bin/python
import os
import sys
import re
import matplotlib.pyplot as plt

def get_data(filename):
    x = []
    y = []
    z = []
    if os.path.exists(filename):
        f = open(filename)
        for l in f.readlines():
            l = re.split(',',l)
            x.append(int(l[0]))
            y.append(int(l[1]))
            z.append(int(l[2]))
    return (x,y,z)

def filter_data(x,window_size=64):
    lenth = len(x)
    i = 0
    ret = []
    while(i < lenth):
        if i + window_size > lenth:
            break
        sum_d = 0
        for y in range(window_size):
            sum_d += x[i + y]
        ret.append((sum_d/window_size))
        #i = i + 1
        i = i + window_size 
    return ret

x,y,z = get_data(sys.argv[1])

y = filter_data(y,window_size=64)
x = filter_data(x,window_size=64)
z = filter_data(z,window_size=64)


plt.figure()
plt.plot(range(len(y)),y,color='red')
plt.plot(range(len(x)),x,color='green')
plt.plot(range(len(z)),z,color='blue')
plt.show()
