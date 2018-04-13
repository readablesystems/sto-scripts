#!/usr/bin/env python

import pandas
import numpy as np
from matplotlib import pyplot as plt

def get_data_serieses(filename):
    data = pandas.read_csv(filename, names=['xput', 'opt'])
    xput = data.xput.tolist()
    opt = data.opt.tolist()

    return (xput[1:], opt[1:])

def draw_lines(xput1_series, xput2_series, opt_series):
    fig, ax1 = plt.subplots(figsize=(10,6))
    N1 = len(xput1_series)
    N2 = len(xput2_series)

    N = N1
    if N2 < N1:
        N = N2

    x_series = np.arange(N)
    x_series *= 10

    lines = []

    lines.append(ax1.plot(x_series, xput1_series[0:N], color='blue'))
    lines.append(ax1.plot(x_series, xput2_series[0:N], color='black'))
    ax1.set_ylim(ymin=0)
    ax1.set_title('TAdaptive warm up chart (w/ TNonopaque)')
    ax1.set_ylabel('Throughput (x100 txns/sec)')

    ax1.set_xlabel('time (ms)')

    ax2 = ax1.twinx()
    ax2.plot(x_series, opt_series[0:N], color='red')
    ax2.set_ylim(ymin=0, ymax=100)
    ax2.set_ylabel('Optimistic reads (%)', color='red')
    ax2.tick_params('y', colors='red')
    
    ax1.set_xlim(0, N*10)

    ax1.legend([l[0] for l in lines], ['TAdaptive', 'TNonopaque'], loc='best')

    fig.tight_layout()
    #plt.show()
    plt.savefig('rate_chart_with_tnonopaque.pdf')

if __name__ == '__main__':
    data1 = get_data_serieses('progress.csv')
    data2 = get_data_serieses('nonopaque_progress.csv')
    draw_lines(data1[0], data2[0], data1[1])
