def sliding_window(image, window_size, stride=1):
    """
    Extracts patches from a grayscale image using a sliding window.

    Parameters:
        image (np.ndarray): Input 2D grayscale image.
        window_size (tuple): Size of the window (height, width).
        stride (int): Stride of the sliding window.

    Returns:
        List of tuples: ((i, j), patch) for each window position.
    """
    h, w = image.shape
    wh, ww = window_size
    patches = []

    for i in range(0, h - wh + 1, stride):
        for j in range(0, w - ww + 1, stride):
            patch = image[i:i+wh, j:j+ww]
            patches.append(((i, j), patch))
    
    return patches
