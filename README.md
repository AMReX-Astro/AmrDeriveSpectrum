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
energy spectrum from a MAESTRO plotfile:

```
$ ./AmrDeriveSpectrum3d.gnu.MPI.ex input_spectrum3d
$ paste -d ' ' x_vel_spectrum_dw.dat y_vel_spectrum_dw.dat z_vel_spectrum_dw.dat > all_spectrum.dat
$ python spectra.py
```

For license information, see the included file `OpenSource.txt`.
