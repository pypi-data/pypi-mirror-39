from scipy.signal import fftconvolve
from skimage import img_as_float
from skimage.io import imread

import dtcwt
import numpy as np


def iubsplet2d(image, order='cubic', level=4):
    """
    Applies the 2D isotropic undecimated b-spline wavelet transform in
    an input image.

    Parameters
    ----------
    image : (N, M) ndarray
        Grayscale input image.
    order : string, optional
        Order of the B-spline filter to be used in the decomposition.
        Accepts the strings 'null' (filter [1]), 'linear' ([1, 2, 1]),
        'cubic' ([1, 4, 6, 4, 1]), 'quintic' ([1, 6, 15, 20, 15, 6, 1]),
        'septic' ([1, 8, 28, 56, 70, 56, 28, 8, 1]), and 'nonic'
        ([1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]). Default is
        'cubic'.
    level : int, optional
        Number of decomposition levels to apply. Default is 4.

    Returns
    -------
    approx : (level, N, M) ndarray
        Array containing the low-pass approximation (smoothing)
        coefficients of the input image, for each level.
    detail : (level, N, M) ndarray
        Array containing the detail B-spline wavelet coefficients
        related to the input image, for each level.

    References
    ----------
    .. [1] Starck, J-L., Murtagh, F. and Bertero, M. "Starlet transform
    in Astronomical Data Processing", in Handbook of Mathematical Methods
    in Imaging, pp 2053-2098. Springer, 2015. doi:
    10.1007/978-1-4939-0790-8_34.
    .. [2] de Siqueira, A.F. et al. Jansen-MIDAS: a multi-level
    photomicrograph segmentation software based on isotropic undecimated
    wavelets, 2016.
    .. [3] de Siqueira, A.F. et al. Estimating the concentration of gold
    nanoparticles incorporated on Natural Rubber membranes using Multi-Level
    Starlet Optimal Segmentation. Journal of Nanoparticle Research, 2014,
    16: 2809. doi: 10.1007/s11051-014-2809-0.

    Examples
    --------
    >>> from skimage.data import camera
    >>> from ubsplet.wavelet import iubsplet2d
    >>> image = camera()
    >>> approx, detail = iubsplet2d(image,
                                    order='quintic',
                                    level=3)

    >>> from skimage.data import coins
    >>> from ubsplet.wavelet import iubsplet2d
    >>> image = coins()
    >>> approx, detail = iubsplet2d(image,
                                    order='linear')
    """

    # check if the image is grayscale.
    if image.shape[-1] in (3, 4):
        raise TypeError('Your image seems to be RGB (shape: {0}). Please'
                        'use a grayscale image.'.format(image.shape))

    if type(image) is np.ndarray:
        image = img_as_float(image)
    elif type(image) is str:
        try:
            image = imread(image, as_grey=True)
        except:
            print('Data type not understood. Please check the input'
                  'data.')
            raise

    # allocating space for approximation and detail results.
    row, col = image.shape
    approx, detail = [np.empty((level, row, col)) for n in range(2)]

    # selecting filter h, based on the chosen b-spline order.
    h_filter, _ = bspline_filters(order)

    # mirroring parameter: lower pixel number.
    if (row < col):
        par = row
    else:
        par = col

    aux_aprx = np.pad(image, (par, par), 'symmetric')

    for curr_level in range(level):
        prev_img = aux_aprx
        h_atrous = atrous_algorithm(h_filter, curr_level)

        # obtaining approximation and wavelet detail coefficients.
        aux_aprx = fftconvolve(prev_img,
                               h_atrous.T*h_atrous,
                               mode='same')
        aux_detl = prev_img - aux_aprx

        # mirroring correction.
        approx[curr_level] = aux_aprx[par:row+par, par:col+par]
        detail[curr_level] = aux_detl[par:row+par, par:col+par]

    return approx, detail


def ubsplet2d(image, order='cubic', level=4):
    """
    Applies the 2D undecimated b-spline wavelet transform in an input
    image.

    Parameters
    ----------
    image : (N, M) ndarray
        Grayscale input image.
    order : string, optional
        Order of the B-spline filter to be used in the decomposition.
        Accepts the strings 'null' (filter [1]), 'linear' ([1, 2, 1]),
        'cubic' ([1, 4, 6, 4, 1]), 'quintic' ([1, 6, 15, 20, 15, 6, 1]),
        'septic' ([1, 8, 28, 56, 70, 56, 28, 8, 1]), and 'nonic'
        ([1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]). Default is
        'cubic'.
    level : int, optional
        Number of decomposition levels to apply. Default is 4.

    Returns
    -------
    aprx : (level, N, M) ndarray
        Array containing the low-pass approximation (smoothing)
        coefficients of the input image, for each level.
    horz : (level, N, M) ndarray
        Array containing the horizontal detail B-spline wavelet
        coefficients related to the input image, for each level.
    vert : (level, N, M) ndarray
        Array containing the vertical detail B-spline wavelet
        coefficients related to the input image, for each level.
    diag : (level, N, M) ndarray
        Array containing the diagonal detail B-spline wavelet
        coefficients related to the input image, for each level.

    References
    ----------
    .. [1] Starck, J-L., Fadili, J. and Murtagh, F. The Undecimated
    Wavelet Decomposition and its Reconstruction. IEEE Transactions on
    Image Processing, 2007, 16(2): 297-309. doi:
    10.1109/TIP.2006.887733.

    Examples
    --------
    >>> from skimage.data import camera
    >>> from ubsplet.wavelet import ubsplet2d
    >>> image = camera()
    >>> aprx, horz, vert, diag = ubsplet2d(image,
                                           order='septic',
                                           level=3)

    >>> from skimage.data import moon
    >>> from ubsplet.wavelet import ubsplet2d
    >>> image = moon()
    >>> aprx, horz, vert, diag = ubsplet2d(image, level=6)
    """

    # check if the image is grayscale.
    if image.shape[-1] in (3, 4):
        raise TypeError('Your image seems to be RGB (shape: {0}). Please'
                        'use a grayscale image.'.format(image.shape))

    if type(image) is np.ndarray:
        image = img_as_float(image)
    elif type(image) is str:
        try:
            image = imread(image, as_grey=True)
        except:
            print('Data type not understood. Please check the input'
                  'data.')
            raise

    # allocating space for approximation and detail results.
    row, col = image.shape
    aprx, horz, vert, diag = [np.empty([level, row, col]) for n in range(4)]

    # selecting filters h and g, based on the chosen b-spline order.
    h_filter, g_filter = bspline_filters(order)

    # mirroring parameter: lower pixel number.
    if (row < col):
        par = row
    else:
        par = col

    aux_aprx = np.pad(image, (par, par), 'symmetric')

    for curr_level in range(level):
        prev_img = aux_aprx
        h_atrous = atrous_algorithm(h_filter, curr_level)
        g_atrous = atrous_algorithm(g_filter, curr_level)

        # obtaining approximation and wavelet detail coefficients.
        aux_aprx = fftconvolve(prev_img,
                               h_atrous.T*h_atrous,
                               mode='same')
        aux_horz = fftconvolve(prev_img,
                               g_atrous.T*h_atrous,
                               mode='same')
        aux_vert = fftconvolve(prev_img,
                               h_atrous.T*g_atrous,
                               mode='same')
        aux_diag = fftconvolve(prev_img,
                               g_atrous.T*g_atrous,
                               mode='same')

        # mirroring correction.
        aprx[curr_level] = aux_aprx[par:row+par, par:col+par]
        horz[curr_level] = aux_horz[par:row+par, par:col+par]
        vert[curr_level] = aux_vert[par:row+par, par:col+par]
        diag[curr_level] = aux_diag[par:row+par, par:col+par]

    return aprx, horz, vert, diag


def atrous_algorithm(input_vector, factor=0):
    """
    Applies the a trous (with holes) algorithm in an 1D array. The a
    trous algorithm inserts 2**i-1 zeros between the elements zeros
    between the array elements, according to the chosen factor.

    Parameters
    ----------
    input_vector : array
        1D input array.
    factor : int, optional
        Number of factors to use on the algorithm. Default is 0.

    Returns
    -------
    atrous_vector : array
        The original input array modified by the a trous algorithm,
        according to the desired factor.

    References
    ----------
    .. [1] Holschneider, M., Kronland-Martinet, R., Morlet, J. and
    Tchamitchian P. "A real-time algorithm for signal analysis with the
    help of the wavelet transform", in Wavelets, Time-Frequency Methods
    and Phase Space, pp. 289–297. Springer-Verlag, 1989.
    .. [2] Shensa, M.J. The Discrete Wavelet Transform: Wedding the À
    Trous and Mallat Algorithms. IEEE Transactions on Signal Processing,
    40(10): 2464-2482, 1992. doi: 10.1109/78.157290.
    .. [3] Mallat, S. A Wavelet Tour of Signal Processing (3rd edition).
    Academic Press, 2008.

    Examples
    --------
    >>> from ubsplet.utils import atrous_algorithm
    >>> import numpy as np
    >>> vec1 = np.array([1, 3, 1])
    >>> atrous_vec1 = atrous_algorithm(vec1, factor=2)

    >>> from ubsplet.utils import atrous_algorithm
    >>> import numpy as np
    >>> vec2 = np.array([2, 1])
    >>> atrous_vec2 = atrous_algorithm(vec2, factor=4)
    """

    if factor == 0:
        atrous_vector = np.copy(input_vector)
    else:
        m = input_vector.size
        atrous_vector = np.zeros(m+(2**factor-1)*(m-1))
        # zeroes array depends on vector size and wavelet level.
        k = 0
        for j in range(0, m+(2**factor-1)*(m-1), (2**factor-1)+1):
            atrous_vector[j] = input_vector[k]
            k += 1

    # 2D vectors requires less effort for applying wavelets.
    return np.atleast_2d(atrous_vector)


def bspline_filters(order='cubic'):
    """
    Returns the pair of filters (h, g), where h is the B-spline filter
    chosen by its order and g is the difference between the Kronecker
    delta function and h.

    Parameters
    ----------
    order : string, optional
        Order of the B-spline filter to be used in the decomposition.
        Accepts the strings 'null' (filter [1]), 'linear' ([1, 2, 1]),
        'cubic' ([1, 4, 6, 4, 1]), 'quintic' ([1, 6, 15, 20, 15, 6, 1]),
        'septic' ([1, 8, 28, 56, 70, 56, 28, 8, 1]), and 'nonic'
        ([1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]). Default is
        'cubic'.

    Returns
    -------
    h_filter : array
        The B-spline filter, according to order.
    g_filter : array
        The difference between the Kronecker delta function and
        h_filter.

    References
    ----------
    .. [1]
    .. [2]

    Examples
    --------
    >>> from ubsplet.utils import bspline_filters
    >>> h_linear, g_linear = bspline_filters(order='linear')
    >>> h_nonic, g_nonic = bspline_filters(order='nonic')
    """

    order2filter = {
        'null': np.array([1]),
        'linear': np.array([1, 2, 1]),
        'cubic': np.array([1, 4, 6, 4, 1]),
        'quintic': np.array([1, 6, 15, 20, 15, 6, 1]),
        'septic': np.array([1, 8, 28, 56, 70, 56, 28, 8, 1]),
        'nonic': np.array([1, 10, 45, 120, 210, 252, 210, 120,
                           45, 10, 1])
    }
    h_filter = order2filter.get(order, None)
    h_filter = h_filter / h_filter.sum()

    try:
        delta = np.zeros(h_filter.shape)
        delta[get_middleindex(delta)] = 1
        g_filter = delta - h_filter
    except:
        print('Sorry. B-spline order not understood')
        raise

    return h_filter, g_filter


def get_middleindex(input_vector):
    """
    Support function. Helps to determine the central element
    of a filter.

    Input: a filter which size will be determined (filter).
    Output: the index of the middle element.
    """

    return int(np.trunc(len(input_vector) / 2))


def uwt2d(image, kind='iso', order='cubic', level=6):
    '''
    2D undecimated wavelet transform.

    Input:  2D image (image).
            number of decomposition levels (level).
    Output: directional wavelet and approximation coefficients
    (aprx, horz, vert, diag).
    '''

    if kind is 'iso':
        aprx, detl = iubsplet2d(image, order, level)
        return aprx, detl
    elif kind is 'und':
        aprx, horz, vert, diag = ubsplet2d(image, order, level)
        return aprx, horz, vert, diag
    else:
        print('Sorry. Wavelet type not understood')
        return None


def uwt3d(images, kind='iso', order='cubic', level=6):
    """
    3D undecimated wavelet transform. Allows to apply UWT on
    a set of images.

    Input:
    Output:
    """

    depth, row, col = np.shape(images)

    if kind is 'iso':
        aprx, detl = [np.empty([depth, level, row, col]) for n in range(2)]

        for cross in range(depth):
            aprx[cross], detl[cross] = uwt2d(images[cross], kind, order, level)
        return aprx, detl
    elif kind is 'und':
        aprx, horz, vert, diag = [np.empty([depth, level, row, col]) for n in range(4)]

        for cross in range(depth):
            aprx[cross], horz[cross], vert[cross], diag[cross] = uwt2d(images[cross], kind, order, level)
        return aprx, horz, vert, diag
    else:
        print('Sorry. Wavelet type not understood')
        return None


def dtcwt2d(img_input, level=6):
    '''


    Input:  2D image (img_input).
            number of decomposition levels (level).
    Output: 
    '''

    trans = dtcwt.Transform2d()
    img_trans = trans.forward(img_input, nlevels=level)

    return img_trans


def dtcwt3d(mat_input, level=6):
    '''

    Input: 
    Output: 
    '''

    depth, _, _ = np.shape(mat_input)

    trans = dtcwt.Transform2d()

    output = list()

    for cross in range(depth):
        output.append(trans.forward(mat_input[cross], nlevels=level))

    return output


def rsmwt3d(mat_input, level=6):
    '''
    Variant version from DT-CWT. Check it at:
    https://dtcwt.readthedocs.org/en/0.11.0/variant.html

    Input: 
    Output: 
    '''

    depth, _, _ = np.shape(mat_input)

    trans = dtcwt.Transform2d(biort='near_sym_b_bp', qshift='qshift_b_bp')

    output = list()

    for cross in range(depth):
        output.append(trans.forward(mat_input[cross], nlevels=level))

    return output

