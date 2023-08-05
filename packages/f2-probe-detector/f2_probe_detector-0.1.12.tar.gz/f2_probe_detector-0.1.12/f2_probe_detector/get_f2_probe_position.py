#!/usr/bin/env
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from astropy.io import fits
from scipy import ndimage


def main():

    pargs = _parse_arguments()

    get_f2_probe_position(
        list_of_files=pargs.files,
    )


def get_f2_probe_position(list_of_files):

    table_header = '{:40} {:10} {:10}'.format('filename', 'x', 'y')

    print(table_header)
    print(len(table_header) * '-')

    for _file in list_of_files:

        hdu = fits.open(_file)

        array = hdu[1].data[0]
        header = hdu[1].header

        # Pre-process data
        circle_mask = CircleMask()
        masked_array = circle_mask.mask_array(array)

        # Filter and mask
        probe_image = get_probe_head(masked_array)
        x, y = get_center_of_mass(probe_image)

        table_row = '{:40s} {:10.5f} {:10.5f}'.format('...' + _file[-37:], x, y)

        print(table_row)


def get_center_of_mass(image):
    """
    Measures center of the object using center the first image momenta
    M00, M01 and M10, defined by:

    M(p,q) = sum_p sum_q i^p * j*q * I(p, q)

    The object's center of mass is the defined by:

    <center_row> = M(1,0) / M(0,0)
    <center_col> = M(0,1) / M(0,0)

    Parameters
    ----------
        image : ndarray

    Returns
    -------
        tuple of floats
            x and y coordinates of the center of mass.
    """
    h, w = image.shape
    grid_row, grid_col = np.mgrid[0:h, 0:w]

    m_00 = image.sum()

    m_10 = (grid_col * image).sum()
    center_row = m_10 / m_00

    m_01 = (grid_row * image).sum()
    center_col = m_01 / m_00

    return center_row, center_col


def get_probe_head(image):
    """
    This method masks the image by subtracting the whole image by its median
    and inverting the grayscale by multiplying it by -1. Then it sets the values
    of the pixels that are below to 1/2 standard deviation to zero. The other pixels
    keep their original value.

    Finally, it applies `grey_opening` to eliminate eventual noisy pixels that does not
    belong to the probe.

    Parameters
    ----------
        image : ndarray
            Sliced and filtered 2D ndarray.

    Returns
    -------
        ndarray
            Masked array.
    """

    # im_filtered = ndimage.median_filter(image, 1, mode='nearest')
    im_bias = np.ma.median(image)
    im_bias_corrected = - (image - im_bias)
    im_thresh = np.ma.where(im_bias_corrected > 0.25 * im_bias, 1, 0)
    im_open = ndimage.morphology.binary_opening(im_thresh)
    im_edt = ndimage.morphology.distance_transform_edt(im_open,
                                                       return_distances=True)

    im_head = np.where(im_edt > 0.5 * im_edt.max(), 1, 0)
    im_head = ndimage.morphology.grey_closing(im_head, 20)

    image = im_bias_corrected * im_head

    return image


def get_shifted_image(image, dx, dy):
    """
    Shift the image using `scipy.interpolation`.

    Parameters
    ----------
        image : ndarray
            2d ndarray containing the image
        dx : float
            shift size in x
        dy : float
            shift size in y

    Returns
    -------
        ndarray
            shifted image
    """
    return ndimage.shift(image, (dy, dx), order=5, mode='nearest')


def _parse_arguments():
    """
    Parse the argument given by the user in the command line.

    Returns
    -------
        pargs : Namespace
            A namespace containing all the parameters that will be used for
            the "detect_probe" function.
    """
    parser = argparse.ArgumentParser(
        description='Find the (x, y) position of the Flamingos 2 guide probe,'
        ' also known as "On-Instrument Wavefront Sensor."'
    )

    parser.add_argument('files', metavar='files', type=str, nargs='+',
                        help="input filenames.")

    return parser.parse_args()


class CircleMask:

    x = 1024
    y = 1024
    radius = 1024

    def mask_array(self, array):

        height, width = array.shape
        y_grid, x_grid = np.mgrid[0:height, 0:width]
        r_grid = np.sqrt((x_grid - self.x) ** 2 + (y_grid - self.y) ** 2)

        masked_array = np.ma.masked_where(r_grid > self.radius, array)

        return masked_array


if __name__ == '__main__':
    main()