from itertools import chain, combinations, product
from math import atan2
from operator import itemgetter
from .tools import angles_in_route, pixels_and_neighbors
from skimage.draw import line
from skimage.measure import label, regionprops
from skimage.graph import route_through_array

import numpy as np
import statistics as stats


def pixels_interest(image):
    """Returns the pixels on intersections and extremities of a
    skeletonized binary image.

    Parameters
    ----------
    image : (N, M) ndarray
        Binary input image.

    Returns
    -------
    px_extreme : list
        Pixels on the extremities of each region.
    px_intersect : list
        Pixels on the intersections of each region.

    Examples
    --------
    >>> from skimage import data
    >>> from skimage.morphology import skeletonize
    >>> from skimage.util import invert
    >>> import matplotlib.pyplot as plt
    >>> image = invert(data.horse())
    >>> img_skel = skeletonize(image)
    >>> px_ext, px_int = pixels_interest(img_skel)
    >>> plt.imshow(img_skel, cmap='gray')
    >>> for px in px_int:  # intersection points.
    ...    plt.scatter(px[1], px[0], c='r')
    >>> for px in px_ext:  # extremity points.
    ...    plt.scatter(px[1], px[0], c='g')
    >>> plt.axis('off')
    >>> plt.show()
    """

    px_neighbors = pixels_and_neighbors(image)
    px_extreme, px_intersect = [[] for i in range(2)]

    for pixel in px_neighbors:
        if len(pixel[1]) == 1:
            px_extreme.append(pixel[0])
        if len(pixel[1]) > 2:
            px_intersect.append(pixel[0])

    return px_extreme, px_intersect


def tracks_classify(image, method='weighave'):
    """.

    Parameters
    ----------
    image : (N, M) ndarray
        Binary input image.
    method : string (default : 'weighave')
        The method to be used on track classification. Accepts the values
        'weighave' (weighted average between Euclidean distance and
        variance), 'perpdist' (perpendicular distance between the route
        point and the extreme points), and 'area' (area of the object
        formed by the line between the extreme points and the route).

    Returns
    -------
     : list
        
     : list
        

    Examples
    --------
    >>> 
    """

    px_ext, px_inter = pixels_interest(image)
    trk_mincoefs, trk_points = [[] for i in range(2)]

    # first, checking the extreme pixels.
    if len(px_ext) == 2:  # only one track (two extreme points).
        return None, None

    while len(px_ext):
        trk_coefs, points = [[] for i in range(2)]

        for i, j in combinations(px_ext+px_inter, r=2):
            points.append([i, j])
            route, _ = route_through_array(~image, i, j)

            if method is 'weighave':
                dists, _, angles = track_parameters(i, j, route)
                trk_wave = tracks_coef_weighave(dists[1], angles)
                trk_coefs.append(trk_wave)

            elif method is 'area':
                trk_area = tracks_coef_area(i, j,
                                            route,
                                            image.shape)
                trk_coefs.append(trk_area)

            elif method is 'perpdist':
                trk_pd = tracks_coef_perpdist(i, j, route)
                trk_coefs.append(trk_pd)

            else:
                print('No known method.')
                return None, None

        # get the best candidate, erase the points and repeat.
        min_idx = min(enumerate(trk_coefs), key=itemgetter(1))[0]

        trk_mincoefs.append(trk_coefs[min_idx])
        trk_points.append(points[min_idx])

        for point in points[min_idx]:
            if point in px_ext:
                px_ext.remove(point)

    return trk_mincoefs, trk_points


def tracks_coef_area(pt_a, pt_b, route, img_shape):
    """
    """

    region_area = np.zeros(img_shape)

    # Euclidean line between the two points.
    rows, cols = line(pt_a[0], pt_a[1],
                      pt_b[0], pt_b[1])
    region_area[rows, cols] = True

    # route.
    for pt in route:
        region_area[pt[0], pt[1]] = True

    props = regionprops(label(region_area))

    return props[0].area


def tracks_coef_area_old(pt_a, pt_b, route):
    """
    """

    # Euclidean line between the two points.
    line_r, line_c = line(pt_a[0], pt_a[1],
                          pt_b[0], pt_b[1])

    x = np.append(np.asanyarray(route)[:, 0], line_r)
    y = np.append(np.asanyarray(route)[:, 1], line_c)

    trk_area = 0.5*np.abs(np.dot(x, np.roll(y, 1)) -
                          np.dot(y, np.roll(x, 1)))

    return trk_area


def tracks_coef_weighave(dist, angles):
    """
    """

    track_weighave = (dist + stats.pvariance(angles))/2

    return track_weighave


def tracks_coef_perpdist(pt_a, pt_b, route):
    """
    """

    track_perpdist = 0

    for pt in route:
        track_perpdist += perpendicular_distance(line=(pt_a, pt_b),
                                                 point=pt)

    return track_perpdist


def perpendicular_distance(line, point):
    """Returns the distance between a line and a point, according to the
    perpendicular line through them.

    Parameters
    ----------
    line : (2, 2) array, list or tuple
        The extremity points of the line A-B, on the form:
        ((A_begin, A_end), (B_begin, B_end)).
    point : (1, 2) array, list or tuple

    Returns
    -------
    distance : float
        Distance between point and line.

    Examples
    --------
    >>> line = ((1, 3), (2, 5))
    >>> perp_dist = perpendicular_distance(line, point=(4, 7))
    """

    pt_a, pt_b = np.asanyarray(line)
    point = np.asanyarray(point)

    distance = np.linalg.norm(np.cross(pt_b - pt_a,
                                       pt_a - point)) / \
        np.linalg.norm(pt_b - pt_a)

    return distance


def track_parameters(first_px, last_px, route):
    """
    """

    dist_px = np.linalg.norm(np.array(first_px) - np.array(last_px))
    dist_diff = np.abs(dist_px-len(route))

    angles = angles_in_route(first_px, route)
    d_row = first_px[0] - last_px[0]
    d_col = first_px[1] - last_px[1]
    angle_px = atan2(d_col, d_row)

    return (dist_px, dist_diff), angle_px, angles
