#!/usr/bin/env python
import math
import numpy

import matplotlib
matplotlib.use("Agg")

from cycler import cycler
import matplotlib.pyplot as plt
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infiles', type=str, nargs='+', help='Name of input spectra .dat files to plot on the same figure after processing with AmrDeriveSpectrum.')
parser.add_argument('-c', '--colors', type=str, nargs='+', help='Sequence of colors for plotting multiple spectra files.')
parser.add_argument('-l', '--legend', type=str, nargs='+', help='Sequence of legend titles for plotting multiple spectra files.')
parser.add_argument('-k', '--show_kolmogorov', action='store_true', help='Overplot the Kolmogorov scaling relation intersecting the energy maximum.')
args = parser.parse_args()

def getFileParams(filename):

    # get the number of lines and fields in the data file
    # skip comment and blank lines, and also, require that
    # the time (first field) is monotonically increasing

    mf = open(filename, "r")

    numLines = 0
    numFields = -1

    oldTime = -1.0

    for line in mf:
        if (not (line.startswith("#") or line.lstrip() == "")):

            fields = line.split()
            time = float(fields[0])

            if (numFields == -1):
                numFields = len(fields)
                oldTime = time
                numLines += 1

            elif (time > oldTime):
                oldTime = time
                numLines +=1

    mf.close()

    return numLines, numFields


def getData(filename):

    # get the data from the data file
    # skip comment and blank lines, and also, require that
    # the time (first field) is monotonically increasing

    numLines, numFields = getFileParams(filename)

    data = numpy.zeros( (numLines, numFields), numpy.float64)

    mf = open(filename, "r")

    indexLine = 0

    oldTime = -1.0

    for line in mf:
        if (not (line.startswith("#") or line.lstrip() == "")):

            fields = line.split()
            time = float(fields[0])

            if (oldTime == -1.0):
                data[indexLine,:] = fields
                oldTime = time
                indexLine += 1

            elif (time > oldTime):
                data[indexLine,:] = fields
                oldTime = time
                indexLine +=1

    mf.close()

    return data


def do_diagnostics():
    # setup plotting
    if args.colors:
        plots_cycler = (cycler(color=args.colors) * cycler(linestyle=['-', '--']))
    else:
        plots_cycler = (cycler(color=['b', 'g', 'r', 'c', 'm', 'k']) * cycler(linestyle=['-', '--']))

    fig = plt.figure()
    # fig.set_figheight(6.0)
    # fig.set_figwidth(8.0)
    ax = fig.add_subplot(111)
    ax.set_prop_cycle(plots_cycler)

    # read data
    for i, infile in enumerate(args.infiles):
        specFile = infile

        specData = getData(specFile)

        Ek = specData[:,1] + specData[:,3] + specData[:,5]

        # plot the simulation data
        if args.legend:
            try:
                label = args.legend[i]
                fit_label = label + ", " + r"$k^{-5/3}$"
            except:
                label = r"spectrum"
                fit_label = r"$k^{-5/3}$"
        else:
            label = r"spectrum"
            fit_label = r"$k^{-5/3}$"

        ax.plot(specData[:,0], Ek, label=label)

        if args.show_kolmogorov:
            # do a crude "fit" using the energy maximum
            n = numpy.argmax(Ek)
        else:
            n = 10
        k = numpy.arange(1000) + 10
        Efit = Ek[n]*(specData[n,0]/k)**(5./3.)

        ax.plot(k, Efit, label=fit_label, alpha=0.5)


    # axis stuff
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlim(1, 5000)
    #ax.set_ylim(1.e9,1.e12)

    ax.set_xlabel(r"$k$")

    ax.set_ylabel(r"$E(k)$")

    leg = ax.legend(loc=1)
    ltext = leg.get_texts()
    # plt.setp(ltext, fontsize=12)
    leg.draw_frame(0)

    plt.tight_layout()

    plt.savefig("spectrum.png", dpi=300)
    plt.savefig("spectrum.eps")


if __name__== "__main__":
    do_diagnostics()
