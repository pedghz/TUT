import numpy as np
import matplotlib.pyplot as plt

with open("targets_5.txt") as f:
    lines = f.readlines()

    x = [line.split()[0] for line in lines]
    # x = [x[18],x[21],x[29],x[22],x[25]]
    y = [line.split()[1] for line in lines]
    # y = [y[18],y[21],y[29],y[22],y[25]]

    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_title("Plot title")
    ax1.set_xlabel('x label')
    ax1.set_ylabel('y label')

    ax1.plot(x,y, c='r', marker='*', label='the data')

    leg = ax1.legend()

    plt.show()