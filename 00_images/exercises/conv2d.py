import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    """
    Performs 2D convolution on a grayscale image using a given kernel.

    Parameters:
        image (np.ndarray): Input 2D image.
        kernel (np.ndarray): Convolution kernel.
        stride (int): Stride for convolution.
        padding (int): Zero-padding around the image.

    Returns:
        np.ndarray: Convolved output.
    """
    image_padded = np.pad(image, pad_width=padding, mode='constant')
    kernel_height, kernel_width = kernel.shape
    img_height, img_width = image_padded.shape
    out_height = (img_height - kernel_height) // stride + 1
    out_width = (img_width - kernel_width) // stride + 1

    output = np.zeros((out_height, out_width))

    for i in range(out_height):
        for j in range(out_width):
            region = image_padded[i*stride:i*stride+kernel_height, j*stride:j*stride+kernel_width]
            output[i, j] = np.sum(region * kernel)
    
    return output
