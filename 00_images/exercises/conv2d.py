import numpy as np

def conv2d_pad(img, kernel, pad='same'):
    h, w = img.shape                  # Get height and width of the input image
    kh, kw = kernel.shape            # Get height and width of the kernel

    if pad == 'same':
        # Compute padding required on height and width to keep output the same size as input
        ph = (kh - 1) // 2
        pw = (kw - 1) // 2
        # Pad the image with zeros using computed padding values
        img_pad = np.pad(img, ((ph, ph), (pw, pw)), mode='constant')
    else:
        # No padding applied
        img_pad = img

    out = np.zeros((h, w))           # Initialize the output array

    # Slide the kernel over each spatial location in the image
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            # Extract the local region and apply element-wise multiplication with the kernel
            out[y, x] = np.sum(img_pad[y:y+kh, x:x+kw] * kernel)

    return out                        # Return the convolved output

def conv2d_stride(img, kernel, pad='same', stride=1):
    h, w, c = img.shape                   # Input image dimensions (height, width, channels)
    kh, kw, kc, oc = kernel.shape        # Kernel dimensions: height, width, in_channels, out_channels

    if pad == 'same':
        # Calculate padding to ensure output has same spatial dimensions as input
        ph = ((h - 1) * stride + kh - h) // 2
        pw = ((w - 1) * stride + kw - w) // 2
        # Pad only height and width dimensions, not channel
        img_pad = np.pad(img, ((ph, ph), (pw, pw), (0, 0)), mode='constant')
    else:
        img_pad = img

    # Compute output height and width using standard convolution formula
    oh = (h + 2 * ph - kh) // stride + 1
    ow = (w + 2 * pw - kw) // stride + 1

    out = np.zeros((oh, ow, oc))         # Initialize output with shape (height, width, out_channels)

    # Iterate over output channels
    for o_c in range(oc):
        for y in range(oh):
            for x in range(ow):
                # Perform element-wise multiplication with the input region and kernel for this output channel
                out[y, x, o_c] = np.sum(
                    img_pad[y*stride:y*stride+kh, x*stride:x*stride+kw, :] * kernel[:, :, :, o_c]
                )

    return out                            # Return the multi-channel convolved output
