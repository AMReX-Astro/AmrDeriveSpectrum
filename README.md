# AmrDeriveSpectrum

AmrDeriveSpectrum calculates the spectrum of variables in an AMReX plotfile.

It depends on the following:

- MPI and its headers should be installed. AmrDeriveSpectrum works
  with mpich.  The path to the MPI library is supplied to AMReX via MPI_HOME.
  It should contain `include` and `lib` as subdirectories.

- FFTW2 and its headers should be installed.  FFTW2 should have been
  compiled with MPI support with double precision.  The path to the
  FFTW2 installation directory is supplied via FFTW2_HOME and it
  should contain `include` and `lib` as subdirectories.

- The amrex source code should be available, supplied via AMREX_HOME.

## Building

To build the executable with the paths to dependencies, do, e.g.:

```
$ make DIM=3 AMREX_HOME=[path-to-amrex] FFTW2_HOME=[path-to-fftw2] MPI_HOME=[path-to-mpi]
```

## Running

The following example uses AmrDeriveSpectrum to calculate the kinetic
energy spectra from two MAESTRO plotfiles.

First, here is the input file for AmrDeriveSpectrum. This example
gives two plotfiles in the working directory, where (x,y,z) velocity
components are stored as variables named "x_vel", "y_vel", and
"z_vel". The spectra are weighted by density.

```
##-----------------------------------------------------------
## INPUT PARAMETERS FOR AMRDERIVESPECTRUM PROBLEM
##-----------------------------------------------------------

# Verbose flag
verbose = 1

# List of input plotfiles to process
infile = wd_4lev_Tc5-5e8_rhoc4-5e9_plt06605 wd_4lev_Tc5-5e8_rhoc4-5e9_plt09991

# Variables to read from the input plotfiles
vars = x_vel y_vel z_vel

# Flag determining whether div_free
div_free = 0

# Flag determining whether or not to transpose spatial indices
transpose_dp = 0

# Flag sets whether or not to weight by density^(1/3)
density_weighting = 1

# Density field
density = density

# Flag sets whether or not to apply cutoff density
use_cutoff_density = 0

# Cutoff density below which to zero the velocities
cutoff_density = 0.0

# Flag determining whether or not to read a list of
# wavenumbers to filter on.
do_filter = 0

# List of wavenumbers to filter on
# filterWN = 0.0 0.0 0.0

# This sets the finest level to do the FFT (e.g. 0 = use only the coarsest level)
finestLevel = 0
```

Then run AmrDeriveSpectrum with this input file.

```
$ ./AmrDeriveSpectrum3d.gnu.MPI.ex input_spectrum3d
```

AmrDeriveSpectrum will store the calculated spectra in text files with
the `.dat` extension inside each plotfile it processes.

To get the kinetic energy power spectrum we combine the power spectra
for (x,y,z) velocity components as follows. In this example the
spectrum files have `_dw` appended to the names because the input file
enabled the density weighting option. So for each `[plotfile]`, we do:

```
$ paste -d ' ' [plotfile]/x_vel_spectrum_dw.dat [plotfile]/y_vel_spectrum_dw.dat [plotfile]/z_vel_spectrum_dw.dat > [plotfile]/all_spectrum.dat
```

And finally run `spectra.py` passing in a list of input spectrum
files. The option `-c` takes a list of matplotlib colors and `-l`
takes a list of labels, one for each spectrum file provided. The `-k`
flag will also plot the Kolmogorov relation intersecting the maximum
energy point of each spectrum curve for comparison.

```
./spectra.py wd_4lev_Tc5-5e8_rhoc4-5e9_plt06605/all_spectrum.dat wd_4lev_Tc5-5e8_rhoc4-5e9_plt09991/all_spectrum.dat -c b g -l 06605 09991 -k
```

This script saves the kinetic energy spectrum plot as `spectrum.png`.

For license information, see the included file `OpenSource.txt`.