#!/bin/bash
paste -d ' ' $1/x_vel_spectrum_dw.dat $1/y_vel_spectrum_dw.dat $1/z_vel_spectrum_dw.dat > $1/all_spectrum.dat
spectra.py $1

