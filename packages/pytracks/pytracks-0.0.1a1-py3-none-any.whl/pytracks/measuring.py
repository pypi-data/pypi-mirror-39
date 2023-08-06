'''


Author: Alexandre Fioravante de Siqueira
Version: march, 2016
'''

from skimage.measure import regionprops

import math


def measure_tracks(img_label):
    '''


    Input:  2D image (img_input).
            number of decomposition levels (level).
    Output: 
    '''

    region_prop = regionprops(img_label)

    for prop in region_prop:
        y0, x0 = prop.centroid
        orient = prop.orientation

        x1 = x0 + math.cos(orient) * prop.major_axis_length
        y1 = y0 - math.sin(orient) * prop.major_axis_length

    return x0, x1, y0, y1

# def plottracks(img_label):
