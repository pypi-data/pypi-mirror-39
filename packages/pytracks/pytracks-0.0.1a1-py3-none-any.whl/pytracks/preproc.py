'''


Author: Alexandre Fioravante de Siqueira
Version: february, 2016
'''

from skimage import img_as_float
from skimage import exposure

import numpy as np


def histogram_equalization(img, typeeq='histeq'):
    """
    Implements options for histogram equalization.
    Parameters
        img
        typeeq: 'histeq', 'adapteq', 'contstr'

    Returns
        img_eq
    """

    img = img_as_float(img)

    if typeeq is 'histeq':
        img_eq = exposure.equalize_hist(img)
    elif typeeq is 'adapteq':
        img_eq = exposure.equalize_adapthist(img, clip_limit=0.03)
    elif typeeq is 'contstr':
        p2, p98 = np.percentile(img, (2, 98))
        img_eq = exposure.rescale_intensity(img, in_range=(p2, p98))

    return img_eq
