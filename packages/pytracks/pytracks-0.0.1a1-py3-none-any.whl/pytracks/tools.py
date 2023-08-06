"""
 PYTRACKS/TOOLS.PY

Copyright (C) Alexandre Fioravante de Siqueira, 2016

This file is part of pytracks.

pytracks is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sys import platform

from itertools import product
from math import atan2
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage.filters import gaussian_laplace
from skimage import img_as_ubyte, measure
from skimage.color import gray2rgb
from skimage.draw import circle, ellipse, ellipse_perimeter
from skimage.feature import canny
from skimage.io import imread
from skimage.measure import CircleModel, EllipseModel, find_contours, \
                            label, regionprops

import numpy as np
import matplotlib.pyplot as plt


def acquire_dataset(filename, depth=5):
    """Reads a set of images in grayscale. Filenames are supposed to have
    sequential numbers: 'filename1.ext', 'filename2.ext', 'filename3.ext',
    etc.

    Parameters
    ----------
    filename : string
        The name of the first file on the set.
    depth : int (default : 5)
        How much images the function is supposed to read.

    Returns
    -------
    img_dataset : (depth, rows, cols) ndarray
        Set of images read.
    """

    while True:
        try:
            aux = imread(filename, as_grey=True)
            break
        except IOError:
            print('Could not read ', filename, '.')
            filename = input('Please type the name of the first image: ')

    rows, cols = np.shape(aux)

    while True:
        try:
            img_dataset = np.zeros((int(depth), rows, cols))
            break
        except NameError:
            print('Could not determine how much images to read.')
            depth = input('Please type the number of images to read: ')

    img_dataset[0] = aux

    try:
        for stack in range(1, depth):
            aux = filename[:-5] + str(stack + 1) + filename[-4:]
            img_dataset[stack] = imread(aux, as_grey=True)
    except:
        print('Could not read image #{0}.'.format(stack))
        raise

    return img_dataset


def angles_in_route(reference_pt, points):
    """Returns the angles between the reference point and each point on
    a set.

    Parameters
    ----------
    reference_pt : list
        The point to be used as reference when calculating the angles.
    points : list
        A list of points to calculate the angles .

    Returns
    -------
    angles : list
        List containing the angles between reference_pt and each point
        of the points list.
    """

    angles = []

    for point in points:
        d_row = reference_pt[0] - point[0]
        d_col = reference_pt[1] - point[1]
        angles.append(atan2(d_col, d_row))

    return angles


def angles_between_points(points):
    """Returns the angles between each point and the previous one on a
    set.

    Parameters
    ----------
    points : list
        A list of points.

    Returns
    -------
    angles : list
        List containing the angles between each point and the previous
        one.
    """

    angles = []

    for idx, point in enumerate(points):
        d_row = point[0] - points[idx-1][0]
        d_col = point[1] - points[idx-1][1]
        angles.append(atan2(d_col, d_row))

    return angles


def edge_coordinates(image, alg='log', sigma=0.5):
    """Separates the edges of each area in the input image,
    returning the corresponding coordinates.

    Parameters
    ----------
    image : array
        Grayscale input image.
    alg : string, optional (default : 'log')
        Algorithm used to extract edges. Accepts the values 'log', for
        Laplacian of Gaussian, and 'canny', for Canny. Default is 'log'.
    sigma : float, optional (default : 0.5)
        Sigma value used on the algorithm.

    Returns
    -------
    regions : array
        Array containing the regions separated by labeled region.
    edges : list
        List containing the coordinates to the edge points, separated
        according to their region.
    """

    img_label, num_regions = measure.label(image, return_num=True)

    alg2edge = {
        'log': gaussian_laplace(image, sigma),
        'canny': canny(image, sigma)
    }
    edges = alg2edge.get(alg, gaussian_laplace(image, sigma))

    edges = [list() for _ in range(num_regions)]
    rows, cols = img_label.shape
    regions = np.empty((num_regions, rows, cols))

    # separating regions and their edges, according to measure.label()
    for num in range(1, num_regions+1):
        regions[num-1] = img_label == num
        contour = measure.find_contours(regions[num-1], level=0)
        edges[num-1] = contour[0].astype(int).tolist()

    # ordering edge pixels
    for edge in edges:
        # calculating centroid
        cntrd = (sum([pt[0] for pt in edge])/len(edge),
                 sum([pt[1] for pt in edge])/len(edge))
        # sorting by polar angle
        edge.sort(key=lambda pt: atan2(pt[1]-cntrd[1],
                                       pt[0]-cntrd[0]))

    return regions, edges


def enumerate_objects(labels, equal_intensity=True, font_size=30):
    """Generate an image with each labeled region numbered.

    Parameters
    ----------
    labels : (rows, cols) ndarray
        Labeled image.
    equal_intensity : bool, optional (default : True)
        If True, each region on the output image will have the same
        intensity.
    font_size : int, optional (default : 30)
        Font size to be used when numbering.

    Returns
    -------
    img_numbered : (rows, cols) ndarray
        Labeled image with each region numbered.

    Examples
    --------
    >>> from skcv.draw import draw_synthetic_circles
    >>> from skimage.measure import label
    >>> image = draw_synthetic_circles((512, 512), quant=25, seed=0)
    >>> img_label = label(image)
    >>> img_numbered = enumerate_objects(img_label,
                                         equal_intensity=True,
                                         font_size=18)
    """

    # avoiding labels to be modified. 
    aux_label = np.copy(labels)

    # obtaining info from the objects.
    obj_info = []
    for idx in regionprops(aux_label):
        obj_info.append([idx.centroid[0],
                         idx.centroid[1],
                         str(idx.label)])

    # adjusting intensity.
    if equal_intensity:
        aux_label[aux_label != 0] = 127

    # default fonts to be used on each system.
    if platform.startswith('linux'):
        font_name = '/usr/share/fonts/truetype\
                     /liberation/LiberationSans-Bold.ttf'
    elif platform.startswith('win'):
        font_name = 'c:/windows/fonts/arialbd.ttf'
    # elif platform.startswith('darwin'):
        #font_name = ''
    font = ImageFont.truetype(font_name, font_size)

    img_numbered = Image.fromarray(img_as_ubyte(aux_label))
    draw = ImageDraw.Draw(img_numbered)

    # drawing numbers on each region.
    for obj in obj_info:
        draw.text((obj[1], obj[0]), obj[2], fill=255, font=font)

    return img_numbered


def fit_objects(image, fit_obj='circle'):
    """Fits objects in each region of the input image, returning the
    parameters of each object.

    Parameters
    ----------
    image : (N, M) ndarray
        Binary input image.
    fit_obj : string, optional (default : 'circle')
        Object to be fitted on the regions. Accepts the strings 'circle'
        and 'ellipse'.

    Returns
    -------
    image_fit : (N, M, 3) ndarray
        An image with objects in green representing the fitted objects
        labeling each region.
    data_fit : array
        The parameters for each object fitted. Each row corresponds to
        a region present on the input image. Each column represents one
        parameter of the fitted object. For fit_obj='circle', they are
        the coordinates for the center of the circle, and the radius
        (x_center, y_center, radius); for fit_obj='ellipse', they are
        the coordinates for the center of the ellipse, the major and
        minor axis and the orientation (x_center, y_center, minor_axis,
        major_axis, theta).

    Examples
    --------
    >>> from skcv.draw import draw_synthetic_circles
    >>> from skimage import img_as_bool
    >>> image = draw_synthetic_circles((512, 512), quant=20, shades=1,
                                       seed=0)
    >>> image_fit, data_fit = fit_objects(img_as_bool(image),
                                          fit_obj='circle')

    >>> from skcv.draw import draw_synthetic_ellipses
    >>> from skimage import img_as_bool
    >>> image = draw_synthetic_ellipses((512, 512), quant=20, shades=1,
                                        seed=0)
    >>> image_fit, data_fit = fit_objects(img_as_bool(image),
                                          fit_obj='ellipse')
    """

    image_fit = gray2rgb(image)

    # checking labels.
    img_label, num_objects = label(image, return_num=True)

    if fit_obj == 'circle':
        obj = CircleModel()
        data_fit = np.zeros((num_objects, 3))
    elif fit_obj == 'ellipse':
        obj = EllipseModel()
        data_fit = np.zeros((num_objects, 5))

    for num in range(num_objects):
        # finding the contour.
        obj_contour = find_contours(img_label == num+1,
                                    fully_connected='high',
                                    level=0)

        try:
            # modelling image using obtained points.
            obj.estimate(obj_contour[0])
            data_fit[num] = obj.params
            aux_fit = data_fit[num].astype(int)

            if fit_obj == 'circle':
                # drawing circle.
                rows, cols = circle(aux_fit[0], aux_fit[1], aux_fit[2],
                                    shape=image_fit.shape)
                image_fit[rows, cols] = [False, True, False]
            elif fit_obj == 'ellipse':
                # drawing ellipse.
                rows, cols = ellipse_perimeter(aux_fit[0], aux_fit[1],
                                               aux_fit[2], aux_fit[3],
                                               aux_fit[4],
                                               shape=image_fit.shape)
                image_fit[rows, cols] = [False, True, False]
        except TypeError:
            print('No sufficient points on region #', num)

    return image_fit, data_fit


def fit_object_coords(points, fit_obj='circle'):
    """Fits objects in each region of the input image, returning the
    parameters of each object.

    Parameters
    ----------
    points : list
        List containing the coordinates to fit the object.
    fit_obj : string, optional (default : 'circle')
        Object to be fitted on the regions. Accepts the strings 'circle'
        and 'ellipse'.

    Returns
    -------
    obj.params : array
        The parameters for the object fitted. Each column represents one
        parameter of the fitted object. For fit_obj='circle', they are
        the coordinates for the center of the circle, and the radius
        (x_center, y_center, radius); for fit_obj='ellipse', they are
        the coordinates for the center of the ellipse, the major and
        minor axis and the orientation (x_center, y_center, minor_axis,
        major_axis, theta).
    """

    obj2model = {
        'circle': measure.CircleModel(),
        'ellipse': measure.EllipseModel()
    }

    try:
        obj = obj2model.get(fit_obj, measure.CircleModel())
        obj.estimate(np.array(points))
        return obj.params

    except TypeError:
        print('Not sufficient points for fitting an object. Sorry')
        return None


def obtain_neighbors(edges, point, num_neigh=3, step=1):
    """Investigates the directional neighbors of a pixel, searching
    for elements of a set into an image.

    Parameters
    ----------
    edges : array
        Binary input image representing the region edge.
    point : list
        Point coordinates of the central pixel.
    num_neigh : int, optional (default : 3)
        Number of neighbors to obtain in each side.
    step : int, optional (default : 1)
        Space given between one point and the other.

    Returns
    -------
    pts_neigh : list
        List containing the coordinates for each neighbor point
        contained in the edges image.
    """

    pts_neigh = []
    x_zero, y_zero = point
    idx = edges.index([x_zero, y_zero])

    # interest point is the first point of the set
    pts_neigh.append([x_zero, y_zero])

    # ordered edges ease the process
    for num in range(num_neigh):
        pts_neigh.append(edges[idx - (step*num)])
        try:
            pts_neigh.append(edges[idx + (step*num)])
        except IndexError:
            aux_idx = (len(edges)-1)-idx
            pts_neigh.append(edges[aux_idx + (step*num)])

    return pts_neigh


def pixels_and_neighbors(image):
    """Returns true pixels in an binary image, and their neighbors.

    Parameters
    ----------
    image : (rows, cols) ndarray
        Binary input image.

    Returns
    -------
    px_and_neigh : list
        List containing true pixels (first coordinate) and their true
        neighbors (second coordinate).
    """

    true_rows, true_cols = np.where(image)
    true_pixels, px_and_neigh = [], []

    for i, _ in enumerate(true_cols):
        true_pixels.append([true_rows[i], true_cols[i]])

    for pixel in true_pixels:
        aux = []
        possible_neigh = [[pixel[0]-1, pixel[1]-1],
                          [pixel[0]-1, pixel[1]],
                          [pixel[0]-1, pixel[1]+1],
                          [pixel[0], pixel[1]-1],
                          [pixel[0], pixel[1]+1],
                          [pixel[0]+1, pixel[1]-1],
                          [pixel[0]+1, pixel[1]],
                          [pixel[0]+1, pixel[1]+1]]

        for point in possible_neigh:
            if point in true_pixels:
                aux.append(point)

        px_and_neigh.append([pixel, aux])

    return px_and_neigh


def sliding_window(image, window_size=(10, 10), step=5):
    """Returns cropped windows from an input image, according to specified
    window size and step.

    Parameters
    ----------
    image : (rows, cols, depth) ndarray
        Input image.
    window_size : tuple, optional (default : (10, 10))
        Size of each window, in pixels, representing rows and columns.
    step : int, optional (default : 5)
        Step between each cropped window, in pixels.

    Returns
    -------
    crop_windows : list
        List containing the coordinates of the first pixel from each
        window, and the cropped windows.

    References
    ----------
    .. [1] A. Rosebrock's pyimagesearch, "Sliding Windows for Object
    Detection with Python and OpenCV". Available at:
    http://www.pyimagesearch.com/2015/03/23/\
    sliding-windows-for-object-detection-with-python-and-opencv/.

    Examples
    --------
    >>> from matplotlib.animation import ArtistAnimation
    >>> from matplotlib.patches import Rectangle
    >>> from skimage.data import camera
    >>> import matplotlib.pyplot as plt
    >>> image = camera()
    >>> windows = sliding_window(image, window_size=(120, 120), step=50)
    >>> fig, ax = plt.subplots(ncols=1, nrows=1)
    >>> image_set = []
    >>> for _, val in enumerate(windows):
    ...    clone = image.copy()
    ...    _ = ax.imshow(clone, cmap='gray')
    ...    rect = Rectangle((val[0][0], val[0][1]),
    ...                     val[0][0] + 120 - val[0][0],
    ...                     val[0][1] + 120 - val[0][1],
    ...                     fill=False,
    ...                     edgecolor='lawngreen',
    ...                     linewidth=2)
    ...    image_set.append([ax.add_patch(rect)])
    >>> ani = ArtistAnimation(fig, images, interval=50, blit=True,
    ...                       repeat_delay=500)
    >>> plt.show()
    """

    rows, cols = image.shape
    crop_windows = []

    for col, row in product(range(0, cols, step), range(0, rows, step)):
        aux = image[row:row + window_size[0],
                    col:col + window_size[1]]
        if aux.shape != window_size:
            continue
        crop_windows.append([[row, col], aux])

    return crop_windows


def acquire_dataset(image_name, depth):
    """
    acquiredataset(image_name, depth)

    Acquires the images which will be used
    on the 3D representation.

    Returns stack.
    """

    while True:
        try:
            aux = imread(image_name, as_grey=True)
            break
        except:
            print('Could not read image.')
            img_name = input('Please type the name of the first image: ')

    row, col = np.shape(aux)

    while True:
        try:
            images = np.zeros((int(depth), row, col))
            break
        except:
            print('Could not determine the dataset size.')
            depth = input('Please type the number of images on the dataset: ')

    images[0] = aux

    try:
        for stack in range(1, depth):
            aux = image_name[:-5] + str(stack + 1) + image_name[-4:]
            images[stack] = imread(aux, as_grey=True)
    except:
        print('Could not read image #{0}.'.format(stack))
        raise

    return images


def progress_bar(prog, mesg='Please wait...'):
    """
    progressbar(prog, mesg='Please wait...')

    Presents a nice progress bar and a text message.

    Original code by user aviraldg on StackOverflow:
    http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """

    print(' '*int(40), end='')  # resetting current message
    print('\r[{0}{1}] {2}% - '.format('#'*int(prog/10), ' '*int((100-prog)/10),
          prog) + str(mesg), end='')

    return None


def save_info_uwt(bin_h, bin_v, bin_d, stk_plot='n', alg='o'):
    """
    saveinfouwt(bin_h, bin_v, bin_d, stk_plot='n', alg='o')

    Saves UWT results.
    """

    _, _, dep, lev = np.shape(bin_h)

    for num in range(lev):
        if str(stk_plot) is 'y':  # plotting stack
            showstackcont(bin_h[:, :, :, num], cm.gray)
            plt.savefig('stackbin_h'+str(alg)+str(num)+'.png',
                        bbox_inches='tight')
            showstackcont(bin_v[:, :, :, num], cm.gray)
            plt.savefig('stackbin_v'+str(alg)+str(num)+'.png',
                        bbox_inches='tight')
            showstackcont(bin_d[:, :, :, num], cm.gray)
            plt.savefig('stackbin_d'+str(alg)+str(num)+'.png',
                        bbox_inches='tight')

        # plotting cross sections:
        showcrosstest(bin_h[:, :, :, num], cm.gray)
        plt.savefig('crossbin_h'+str(alg)+str(num)+'.png',
                    bbox_inches='tight')
        showcrosstest(bin_v[:, :, :, num], cm.gray)
        plt.savefig('crossbin_v'+str(alg)+str(num)+'.png',
                    bbox_inches='tight')
        showcrosstest(bin_d[:, :, :, num], cm.gray)
        plt.savefig('crossbin_d'+str(alg)+str(num)+'.png',
                    bbox_inches='tight')

    plt.close('all')

    return None


def show_stack_cont(stack, color_map=cm.YlGnBu):
    """
    showstackcont(stack, color_map=cm.YlGnBu)

    Presents the stack visualization based
    on contours.
    """

    row, col, dep = np.shape(stack)

    x = np.linspace(0, row, row)
    y = np.linspace(0, col, col)
    xx, yy = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_zlim(-(dep+1), 1)

    for curr_dep in range(dep):
        ax.contourf(xx, yy, np.transpose(stack[:, :, curr_dep]),
                    zdir='z', offset=-curr_dep, cmap=color_map)

    return None


def dtcwt_nameangle(num_slice):
    num2angle = {
        0: '15 degrees',
        1: '45 degrees',
        2: '75 degrees',
        3: '-75 degrees',
        4: '-45 degrees',
        5: '-15 degrees'
    }
    return num2angle.get(num_slice, 'nothing')
