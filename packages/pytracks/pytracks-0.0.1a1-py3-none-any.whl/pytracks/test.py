from matplotlib import cm


def show_cross_test(images, color_map=cm.YlGnBu):
    """
    showcrosstest(images, color_map=cm.YlGnBu)

    Test function. Plots slices from 'muscovite'
    and 'volcanic glass' test datasets.
    """

    depth, _, _ = np.shape(images)
    pos = 0  # controls subplot position

    # volcanic glass dataset
    if depth == 3:
        for stack in range(depth):
            pos += 1
            plt.subplot(2, 2, pos)
            plt.imshow(images[stack], cmap=color_map)
            plt.axis('off')
    # muscovite dataset
    elif dep == 14:
        for stack in range(depth):
            pos += 1
            plt.subplot(4, 4, pos)
            plt.imshow(images[stack], cmap=color_map)
            plt.axis('off')

    return None
