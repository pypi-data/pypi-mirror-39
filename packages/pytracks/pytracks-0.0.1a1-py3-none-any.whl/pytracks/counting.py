from skimage.measure import regionprops

import numpy as np


def count_tracks_area(labels, max_area=1.5):
    """
    """

    reg_area = []
    mean_area = 0
    num_obj = 0

    regions = regionprops(labels)
    for reg in regions:
        reg_area.append([reg.label, reg.area])
        mean_area += reg.area

    mean_area /= len(regions)
    for area in reg_area:
        area.append(np.trunc(area[1] / (mean_area * max_area)) + 1)

    return reg_area, mean_area
