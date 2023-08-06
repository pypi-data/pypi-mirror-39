"""
"""

from skimage.filters import threshold_otsu, threshold_yen

import numpy as np
import sys


def binary_results(hor, ver, dia, alg='o'):
    """
    """

    row, col, dep, lev = np.shape(hor)
    bin_h, bin_v, bin_d = [np.empty([row, col, dep, lev]) for n in range(3)]

    if str(alg) is 'o':
        for num in range(lev):
            bin_h[:, :, :, num] = binotsustack(hor[:, :, :, num])
            bin_v[:, :, :, num] = binotsustack(ver[:, :, :, num])
            bin_d[:, :, :, num] = binotsustack(dia[:, :, :, num])
    elif str(alg) is 'y':
        for num in range(lev):
            bin_h[:, :, :, num] = binyenstack(hor[:, :, :, num])
            bin_v[:, :, :, num] = binyenstack(ver[:, :, :, num])
            bin_d[:, :, :, num] = binyenstack(dia[:, :, :, num])
    else:
        sys.exit('Algorithm not known (yet).')

    return bin_h, bin_v, bin_d


def binary_otsu_cross(cross):
    """
    binotsucross(cross)

    Applies Otsu's algorithm on an image.
    """

    aux_thres = threshold_otsu(cross)
    bin_cross = (cross <= aux_thres)

    return bin_cross


def binary_otsu_stack(stack):
    """
    binotsustack(stack)

    Applies Otsu's algorithm on a set of images.
    """

    row, col, dep = np.shape(stack)

    bin_stack = np.empty([row, col, dep])

    for cross in range(dep):
        aux_thres = threshold_otsu(stack[:, :, cross])
        bin_stack[:, :, cross] = (stack[:, :, cross] <= aux_thres)

    return bin_stack


def binary_yen_cross(cross):
    """
    binyencross(cross)

    Applies Yen's algorithm on an image.
    """

    aux_thres = threshold_yen(cross)
    bin_cross = (cross <= aux_thres)

    return bin_cross


def binary_yen_stack(stack):
    """
    binyenstack(stack)

    Applies Yen's algorithm on a set of images.
    """

    row, col, dep = np.shape(stack)

    bin_stack = np.empty([row, col, dep])

    for cross in range(dep):
        aux_thres = threshold_yen(stack[:, :, cross])
        bin_stack[:, :, cross] = (stack[:, :, cross] <= aux_thres)

    return bin_stack
