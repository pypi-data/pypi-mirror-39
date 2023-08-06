import astropy.io.fits as pyfits
import astropy.visualization as vis

import matplotlib.pyplot as plt
import numpy as np
import os
import pytest

from scipy import ndimage
import matplotlib.patches as mpatches

import f2_probe_detector as f2


def test_center_of_gravity(show_plots):

    box = Box(35, 20, 10, 30)
    test_array = np.zeros((50, 60))
    test_array[box.bottom:box.top + 1, box.left:box.right + 1] = 100.

    measured_x, measured_y = f2.get_center_of_mass(test_array)

    if show_plots:

        fig, ax = plt.subplots(num=__name__)
        ax.imshow(test_array, origin='lower')
        ax.axvline(box.center_x, color='white', alpha=0.25)
        ax.axhline(box.center_y, color='white', alpha=0.25)
        ax.axvline(measured_x, color='white', alpha=0.25, linestyle='--')
        ax.axhline(measured_y, color='white', alpha=0.25, linestyle='--')

        plt.show()

    assert abs(measured_x - box.center_x) < 1e5
    assert abs(measured_y - box.center_y) < 1e5


def test_shift_image(show_plots):

    shift_x = 5.
    shift_y = 2.

    box = Box(35, 20, 10, 30)
    test_array = np.zeros((50, 60))
    test_array[box.bottom:box.top + 1, box.left:box.right + 1] = 100.

    shifted_array = f2.get_shifted_image(test_array, shift_x, shift_y)
    corrected_array = f2.get_shifted_image(shifted_array, -shift_x, -shift_y)

    reference_x, reference_y = f2.get_center_of_mass(test_array)
    shifted_x, shifted_y = f2.get_center_of_mass(shifted_array)

    if show_plots:

        fig, axs = plt.subplots(num=__name__, ncols=2)

        axs[0].set_title("Reference - Shifted array")
        axs[0].imshow(test_array - shifted_array, origin='lower')
        axs[0].axvline(reference_x, color='white', alpha=0.25)
        axs[0].axhline(reference_y, color='white', alpha=0.25)
        axs[0].axvline(shifted_x, color='white', alpha=0.25, linestyle='--')
        axs[0].axhline(shifted_y, color='white', alpha=0.25, linestyle='--')

        axs[1].set_title("Reference - De-shifted array")
        axs[1].imshow(test_array - corrected_array, origin='lower')

        plt.show()

    np.testing.assert_array_almost_equal(test_array, corrected_array)
    assert abs(reference_x + shift_x - shifted_x) < 1e5
    assert abs(reference_y + shift_y - shifted_y) < 1e5


@pytest.mark.parametrize("filename", ["test_data.fits", "test_data.fits"])
def test_get_array_and_header(filename, datadir):

    filename = "test_data.fits"
    array = f2.get_array(os.path.join(datadir, filename))
    header = f2.get_header(os.path.join(datadir, filename))

    assert isinstance(array, np.ndarray)
    assert isinstance(header, pyfits.Header)


def test_get_probe_head_position_with_fake_data(show_plots):

    probe = Probe(1000, 500)
    head = probe.head
    arm = probe.arm

    # Create fake array
    test_array = np.zeros((2048, 2048))
    test_array[head.bottom:head.top + 1, head.left:head.right + 1] = - 100.
    test_array[arm.bottom: arm.top, arm.left:arm.right] = - 100.

    # Add noise
    test_array = test_array + np.random.normal(0, 50, test_array.shape)
    test_array = test_array + np.random.poisson(size=test_array.shape)
    test_array = ndimage.gaussian_filter(test_array, 3)

    # Filter and mask
    probe_image = f2.get_probe_head(test_array)
    probe_position_x, probe_position_y = f2.get_center_of_mass(probe_image)

    if show_plots:

        fig, axs = plt.subplots(num=__name__, ncols=2)

        axs[0].imshow(test_array, origin="lower")
        axs[0].axvline(probe.head.center_x, color='white', alpha=0.25)
        axs[0].axhline(probe.head.center_y, color='white', alpha=0.25)
        axs[0].axvline(probe_position_x, color='red', alpha=0.25, ls='--')
        axs[0].axhline(probe_position_y, color='red', alpha=0.25, ls='--')

        axs[1].imshow(probe_image, origin="lower")
        axs[1].axvline(probe.head.center_x, color='white', alpha=0.25)
        axs[1].axhline(probe.head.center_y, color='white', alpha=0.25)
        axs[1].axvline(probe_position_x, color='red', alpha=0.25, ls='--')
        axs[1].axhline(probe_position_y, color='red', alpha=0.25, ls='--')

        plt.show()

    assert abs(probe.head.center_x - probe_position_x) < 1e5
    assert abs(probe.head.center_y - probe_position_y) < 1e5


def test_get_probe_head_position_with_fake_shift(show_plots, datadir):

    # Read data
    filename = "test_data.fits"
    ad = pyfits.open(os.path.join(datadir, filename))
    test_array = ad[1].data[0]

    # ad = astrodata.open(os.path.join(datadir, filename))
    # test_array = ad[0].data[0]

    # Pre-process data
    circle_mask = f2.CircleMask()
    masked_array = circle_mask.mask_array(test_array)

    # Filter and mask
    probe_image = f2.get_probe_head(masked_array)
    initial_position_x, initial_position_y = f2.get_center_of_mass(probe_image)

    # Shift data
    shift_x = 0.5
    shift_y = 2.0
    shifted_array = f2.get_shifted_image(test_array, shift_x, shift_y)

    # Do it again
    masked_shifted_array = circle_mask.mask_array(shifted_array)
    probe_image = f2.get_probe_head(masked_shifted_array)
    final_position_x, final_position_y = f2.get_center_of_mass(probe_image)

    # Correct shift
    dx = final_position_x - initial_position_x
    dy = final_position_y - initial_position_y
    corrected_array = f2.get_shifted_image(shifted_array, - dx, - dy)
    residual_array = test_array - corrected_array

    if show_plots:

        fig, axs = plt.subplots(num=__name__, ncols=2)

        n = vis.ImageNormalize(
            data=test_array,
            interval=vis.PercentileInterval(95),
            stretch=vis.LinearStretch()
        )

        axs[0].imshow(test_array, origin="lower", norm=n)
        axs[0].axvline(initial_position_x, color='white', alpha=0.25)
        axs[0].axhline(initial_position_y, color='white', alpha=0.25)

        n = vis.ImageNormalize(
            data=residual_array,
            interval=vis.PercentileInterval(95),
            stretch=vis.LinearStretch()
        )

        axs[1].imshow(residual_array, origin="lower", norm=n)

        plt.show()

    assert test_array.std() >= residual_array.std()
    assert abs(shift_x - dx) < 1.e5
    assert abs(shift_y - dy) < 1.e5


def test_two_images_same_position(show_plots, datadir):

    file_name_1 = 'test_data_same_position1.fits'
    file_name_2 = 'test_data_same_position2.fits'

    test_array_1 = pyfits.open(os.path.join(datadir, file_name_1))[1].data[0]
    test_array_2 = pyfits.open(os.path.join(datadir, file_name_2))[1].data[0]

    # Pre-process data
    circle_mask = f2.CircleMask()
    masked_array_1 = circle_mask.mask_array(test_array_1)
    masked_array_2 = circle_mask.mask_array(test_array_2)

    # Filter and mask
    probe_image_1 = f2.get_probe_head(masked_array_1)
    probe_image_2 = f2.get_probe_head(masked_array_2)

    x_1, y_1 = f2.get_center_of_mass(probe_image_1)
    x_2, y_2 = f2.get_center_of_mass(probe_image_2)

    cx1, cy1, r1 = f2.get_enclosed_circle(probe_image_1)
    cx2, cy2, r2 = f2.get_enclosed_circle(probe_image_2)

    if show_plots:

        box_size = 200
        fig, axs = plt.subplots(num=__name__, ncols=2, nrows=3)

        n = vis.ImageNormalize(
            data=test_array_1,
            interval=vis.PercentileInterval(95),
            stretch=vis.LinearStretch()
        )

        axs[0, 0].imshow(test_array_1, origin="lower", norm=n)
        axs[0, 0].axvline(x_1, color='white', alpha=0.25)
        axs[0, 0].axhline(y_1, color='white', alpha=0.25)

        axs[1, 0].imshow(probe_image_1, origin="lower")
        axs[1, 0].axvline(x_1, color='white', alpha=0.25)
        axs[1, 0].axhline(y_1, color='white', alpha=0.25)
        axs[1, 0].set_xlim(x_1 - box_size / 2, x_1 + box_size / 2)
        axs[1, 0].set_ylim(y_1 - box_size / 2, y_1 + box_size / 2)

        n = vis.ImageNormalize(
            data=test_array_2,
            interval=vis.PercentileInterval(95),
            stretch=vis.LinearStretch()
        )

        axs[0, 1].imshow(test_array_2, origin="lower", norm=n)
        axs[0, 1].axvline(x_2, color='white', alpha=0.25)
        axs[0, 1].axhline(y_2, color='white', alpha=0.25)

        axs[1, 1].imshow(probe_image_2, origin="lower")
        axs[1, 1].axvline(x_2, color='white', alpha=0.25)
        axs[1, 1].axhline(y_2, color='white', alpha=0.25)
        axs[1, 1].set_xlim(x_2 - box_size / 2, x_2 + box_size / 2)
        axs[1, 1].set_ylim(y_2 - box_size / 2, y_2 + box_size / 2)

        diff_image = probe_image_1 - probe_image_2

        axs[2, 0].imshow(diff_image, origin="lower")
        axs[2, 0].set_xlim(x_2 - box_size / 2, x_2 + box_size / 2)
        axs[2, 0].set_ylim(y_2 - box_size / 2, y_2 + box_size / 2)

        circle1 = mpatches.Circle((cx1, cy1), radius=r1,
                                  ec='none', fc='red', alpha=0.20)

        circle2 = mpatches.Circle((cx2, cy2), radius=r2,
                                  ec='none', fc='cyan', alpha=0.20)

        axs[2, 1].imshow(probe_image_1, origin="lower")
        axs[2, 1].set_xlim(x_2 - box_size / 2, x_2 + box_size / 2)
        axs[2, 1].set_ylim(y_2 - box_size / 2, y_2 + box_size / 2)
        axs[2, 1].add_artist(circle1)
        axs[2, 1].add_artist(circle2)

        plt.show()

    assert abs(cx1 - cx2) < 0.20
    assert abs(cy1 - cy2) < 0.20


def test_get_probe_head_using_opencv(show_plots, datadir):

    file_name = 'test_data_same_position1.fits'
    test_array = pyfits.open(os.path.join(datadir, file_name))[1].data[0]

    # Pre-process data
    circle_mask = f2.CircleMask()
    masked_array_1 = circle_mask.mask_array(test_array)

    # Filter and mask
    def get_probe_head(image):

        import cv2 as cv

        im_bias = np.ma.median(image)
        im_bias_corrected = - (image - im_bias)

        temp = np.ma.filled(im_bias_corrected, 0)
        temp = ndimage.median_filter(temp, 5)

        temp = np.uint8((temp - temp.min()) / temp.ptp() * 255)

        ret, thresh = cv.threshold(src=temp, thresh=127, maxval=255,
                                   type=cv.THRESH_BINARY + cv.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

        # sure background area
        sure_bg = cv.erode(opening, kernel, iterations=5)

        # canny edge detection
        temp = opening * sure_bg
        edges = cv.Canny(temp, np.median(temp), np.percentile(temp, 75.))

        _, contours, hierarchy = cv.findContours(edges, mode=cv.RETR_TREE,
                                         method=cv.CHAIN_APPROX_TC89_L1)

        area = 0
        contour = None
        for c in contours:
            c_area = cv.contourArea(c)
            if c_area > area:
                contour = c

        temp = cv.fillPoly(temp, contour, color=255)

        temp = cv.distanceTransform(temp, cv.DIST_L2, 5)
        temp = np.where(temp > 0.5 * temp.max(), temp, 0)
        temp = np.uint8(temp)

        _, contours, hierarchy = cv.findContours(temp, mode=cv.RETR_TREE,
                                                 method=cv.CHAIN_APPROX_TC89_L1)

        area = 0
        contour = None
        for c in contours:
            c_area = cv.contourArea(c)
            if c_area > area:
                contour = c

        (x, y), radius = cv.minEnclosingCircle(contour)

        image = im_bias_corrected

        return image, temp, (x, y, radius)

    probe_image_1, m, circle = get_probe_head(masked_array_1)

    if show_plots:

        import matplotlib.lines as mlines

        fig, axs = plt.subplots(num=__name__, ncols=2)

        n = vis.ImageNormalize(
            data=probe_image_1,
            interval=vis.PercentileInterval(95),
            stretch=vis.LinearStretch()
        )

        axs[0].imshow(probe_image_1, origin="lower")

        axs[1].imshow(m, origin="lower")
        axs[1].axvline(circle[0], color='white', alpha=0.3)
        axs[1].axhline(circle[1], color='white', alpha=0.3)

        c = mpatches.Circle((circle[0], circle[1]), radius=circle[2], ec='none',
                            fc='white', alpha=0.3)
        axs[1].add_artist(c)

        plt.show()


class Box:

    def __init__(self, center_x, center_y, width, height):

        self.center_x = center_x
        self.center_y = center_y

        self.left = center_x - width // 2
        self.right = center_x + width // 2
        self.bottom = center_y - height // 2
        self.top = center_y + height // 2


class Probe:

    def __init__(self, center_x, center_y):

        self.center_x = center_x
        self.center_y = center_y

        self.head = Box(center_x, center_y, 250, 250)

        self.arm = Box(center_x, center_y, 50, 50)
        self.arm.top = self.head.bottom
        self.arm.bottom = 0

        del self.arm.center_x
        del self.arm.center_y

