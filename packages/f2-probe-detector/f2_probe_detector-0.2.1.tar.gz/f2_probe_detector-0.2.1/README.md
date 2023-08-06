# Flamingos 2 Probe Detector

This package contains a single script used to detect the position of the 
Flamingos 2 Guide Probe with sub-pixel accuracy. For that, it uses several 
morphological operations available inside the `scipy.ndimage` package.

The probe position, for now, is obtained using Center of Mass. That means that 
the whole probe image should be displayed. If the Probe Image touches the 
edge of the field of view, the results are unpredictable. 

## Requirements

Before you install this package, make sure your Python environment has all 
the required dependencies:

- Python 3
- astropy
- matplotlib
- numpy
- scipy
- opencv2

The best way of having all of them at once is installing Anaconda and 
AstroConda.

## Install

Once you are inside a `conda` environment, you can install this package by 
simply typing: 

```bash
   # Make sure you activate your virtual environment
   $ source activate $MYENV  
   
   # Install using pip
   $ pip install f2_probe_detector
```

It is highly recommended that you install this package inside a Anaconda 
virtual environment. If possible, install is inside your "astroconda" venv.

## Running

To get information about how to run this script, you can type:

```bash
   $ get_f2_probe_position --help 
```

```bash
   $ get_f2_probe_position file_1.fits file_2.fits ... file_n.fits
   
   filename                                 x          y         
--------------------------------------------------------------
...est_get_f2_probe_position/file_1.fits 1091.43815  583.93075
...est_get_f2_probe_position/file_2.fits 1091.43815  583.93075
...est_get_f2_probe_position/file_3.fits 1091.43815  583.93075
..._get_f2_probe_position/test_data.fits 1091.43815  583.93075
```

or

```bash
   $ get_f2_probe_position file_*.fits
   
   filename                                 x          y         
--------------------------------------------------------------
...est_get_f2_probe_position/file_1.fits 1091.43815  583.93075
...est_get_f2_probe_position/file_2.fits 1091.43815  583.93075
...est_get_f2_probe_position/file_3.fits 1091.43815  583.93075
..._get_f2_probe_position/test_data.fits 1091.43815  583.93075 
```

## Known Issues

1. `get_f2_probe_position` will not fail if cannot find a probe. If you get a 
  very weird value, check the image.
2. `get_f2_probe_position` will not work if the probe shadow touches the edge. 

