"""

"""

from pytracks.test import show_cross_test
from matplotlib import cm
from scipy.ndimage.measurements import label

import matplotlib.pyplot as plt
import numpy as np


def label_stack(bin_h, bin_v, bin_d):
    """
    labelstack(bin_h, bin_v, bin_d)

    Returns: lab_h, lab_v, lab_d
    """

    depth, level, row, col = np.shape(bin_h)
    lab_hor, lab_ver, lab_dia = [np.empty([depth, level, row, col]) for n in range(3)]

    for curr_level in range(level):
        lab_hor[:, curr_level] = label(bin_h[:, curr_level])
        lab_ver[:, curr_level] = label(bin_v[:, curr_level])
        lab_dia[:, curr_level] = label(bin_d[:, curr_level])

    return lab_hor, lab_ver, lab_dia


def show_track(lab_stk, trk_num=0):
    """

    """

    if trk_num is 'all':
        lab_max = np.max(lab_stk)
        count = 0
        while (20*count < lab_max):
            for curr_stk in range(20*count, 20*(count+1)):
                lab_view = (lab_stk == curr_stk)
                plt.figure()
                showcrosstest(lab_view, cm.gray)
                input("Press Enter to continue...")
                count += 1
    else:
        lab_view = (lab_stk == trk_num)
        plt.figure()
        showcrosstest(lab_view, cm.gray)

    return None


def save_track(lab_stk, trk_num=0):
    """
    """

    dep, _, _ = np.shape(lab_stk)
    trk_view = (lab_stk == trk_num)

    for curr_depth in range(depth):
        plt.imshow(trk_view[curr_dep] is True, cmap=cm.gray)
        plt.axis('off')
        plt.savefig('track_n'+str(trk_num)+'_'+str(curr_dep)+'.png',
                    bbox_inches='tight')

    plt.close('all')

    return None
