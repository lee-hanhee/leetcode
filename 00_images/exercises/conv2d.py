import numpy as np

def conv2d_pad(img, kernel, pad='same'):
    """
    Performs 2D convolution with optional padding.
    
    First principles:
    - Convolution slides a kernel over an image and computes the weighted sum at each position
    - Padding adds border pixels to maintain output dimensions
    
    Parameters:
        img (np.ndarray): Input image (2D array)
        kernel (np.ndarray): Convolution filter/kernel (2D array)
        pad (str): 'same' to maintain output size, otherwise no padding
        
    Returns:
        np.ndarray: Convolution result with same dimensions as input
    """
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
    """
    Performs strided 2D convolution with multi-channel support.
    
    First principles:
    - Adds stride parameter to control step size between convolution operations
    - Supports multi-channel input images and multi-channel output
    - Kernel has 4 dimensions: height, width, input channels, output channels
    
    Parameters:
        img (np.ndarray): Input image with shape (h, w, channels)
        kernel (np.ndarray): Filter with shape (kh, kw, in_channels, out_channels)
        pad (str): 'same' for padding that maintains spatial dimensions
        stride (int): Step size for moving the kernel
        
    Returns:
        np.ndarray: Convolution result with shape (output_h, output_w, out_channels)
    """
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
        ph = pw = 0  # No padding

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

def conv2d_general(input_tensor, filters, stride=(1, 1), padding=(0, 0), dilation=(1, 1)):
    """
    Performs general 2D convolution supporting batches, multiple input/output channels.
    
    First principles:
    - Generalizes convolution to handle batches of images
    - Supports separate stride/padding for height and width
    - Includes dilation to increase the receptive field without increasing parameters
    - Core formula: output[b,c_out,h,w] = sum(input[b,c_in,h+dh,w+dw] * filter[c_out,c_in,kh,kw])
    
    Parameters:
        input_tensor (np.ndarray): Shape (batch_size, in_channels, in_height, in_width)
        filters (np.ndarray): Shape (out_channels, in_channels, kernel_height, kernel_width)
        stride (tuple): Stride in height and width directions
        padding (tuple): Padding in height and width directions
        dilation (tuple): Dilation factor for the kernel
        
    Returns:
        np.ndarray: Convolved output with shape (batch_size, out_channels, out_height, out_width)
    """
    # Extract dimensions
    batch_size, in_channels, in_height, in_width = input_tensor.shape
    out_channels, _, kernel_height, kernel_width = filters.shape
    stride_h, stride_w = stride
    padding_h, padding_w = padding
    dilation_h, dilation_w = dilation
    
    # Calculate effective kernel dimensions with dilation
    # Dilation creates "holes" in the kernel, increasing receptive field size
    effective_kernel_h = kernel_height + (kernel_height - 1) * (dilation_h - 1)
    effective_kernel_w = kernel_width + (kernel_width - 1) * (dilation_w - 1)
    
    # Calculate output dimensions using the convolution formula
    out_height = (in_height + 2 * padding_h - effective_kernel_h) // stride_h + 1
    out_width = (in_width + 2 * padding_w - effective_kernel_w) // stride_w + 1
    
    # Pad the input - zeros added around spatial dimensions only
    padded_input = np.pad(
        input_tensor, 
        ((0, 0), (0, 0), (padding_h, padding_h), (padding_w, padding_w)),
        mode='constant'
    )
    
    # Initialize output tensor
    output = np.zeros((batch_size, out_channels, out_height, out_width))
    
    # Perform convolution - this is the core implementation
    for b in range(batch_size):                     # Batch dimension
        for c_out in range(out_channels):           # Output channel dimension
            for h_out in range(out_height):         # Output height dimension
                for w_out in range(out_width):      # Output width dimension
                    # Calculate input region start position with stride
                    h_in = h_out * stride_h
                    w_in = w_out * stride_w
                    
                    # Initialize accumulator for this output position
                    acc = 0
                    
                    # Sum over input channels and kernel dimensions
                    for c_in in range(in_channels):           # Input channel dimension
                        for kh in range(kernel_height):       # Kernel height dimension
                            for kw in range(kernel_width):    # Kernel width dimension
                                # Apply dilation to kernel position
                                h_offset = kh * dilation_h
                                w_offset = kw * dilation_w
                                
                                # Get the input value and filter weight
                                input_val = padded_input[b, c_in, h_in + h_offset, w_in + w_offset]
                                filter_val = filters[c_out, c_in, kh, kw]
                                
                                # Accumulate the product
                                acc += input_val * filter_val
                                
                    # Set the output value
                    output[b, c_out, h_out, w_out] = acc
    
    return output

if __name__ == "__main__":
    print("Testing convolution implementations")
    
    # Test 1: Simple conv2d_pad with edge detection kernel
    print("\n=== Testing conv2d_pad with edge detection ===")
    # Create a simple 6x6 image with a vertical line
    img = np.zeros((6, 6))
    img[:, 2:4] = 1
    print("Input image:")
    print(img)
    
    # Sobel edge detection kernel (horizontal edges)
    edge_kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    
    result = conv2d_pad(img, edge_kernel)
    print("\nEdge detection result:")
    print(result)
    
    # Test 2: Multi-channel convolution with stride
    print("\n=== Testing conv2d_stride with RGB image ===")
    # Create a tiny RGB image (3x3x3)
    rgb_img = np.zeros((3, 3, 3))
    # Red channel with horizontal pattern
    rgb_img[:, :, 0] = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    # Green channel with vertical pattern
    rgb_img[:, :, 1] = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    # Blue channel with center dot
    rgb_img[:, :, 2] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    
    print("RGB Image shape:", rgb_img.shape)
    print("Red channel:\n", rgb_img[:, :, 0])
    print("Green channel:\n", rgb_img[:, :, 1])
    print("Blue channel:\n", rgb_img[:, :, 2])
    
    # Create a simple multi-channel kernel for feature extraction
    # Kernel shape: (height, width, in_channels, out_channels)
    kernel = np.zeros((2, 2, 3, 2))
    # First output channel: detect horizontal lines (sensitive to red channel)
    kernel[:, :, 0, 0] = [[1, 1], [0, 0]]  # Top-sensitive on red
    # Second output channel: detect vertical lines (sensitive to green channel)
    kernel[:, :, 1, 1] = [[1, 0], [1, 0]]  # Left-sensitive on green
    
    # Apply strided convolution
    stride_result = conv2d_stride(rgb_img, kernel, stride=1)
    print("\nStrided convolution result (2 output channels):")
    print("Output shape:", stride_result.shape)
    print("Output channel 1 (horizontal detector):\n", stride_result[:, :, 0])
    print("Output channel 2 (vertical detector):\n", stride_result[:, :, 1])
    
    # Test 3: General convolution with batches and dilation
    print("\n=== Testing conv2d_general with batches and dilation ===")
    # Create a batch of 2 simple images
    batch_input = np.zeros((2, 1, 4, 4))  # (batch, channels, height, width)
    # First image: horizontal line
    batch_input[0, 0] = np.array([
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    # Second image: vertical line
    batch_input[1, 0] = np.array([
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ])
    
    print("Batch input shape:", batch_input.shape)
    print("Image 1:\n", batch_input[0, 0])
    print("Image 2:\n", batch_input[1, 0])
    
    # Create filters for detecting horizontal and vertical lines
    filters = np.zeros((2, 1, 2, 2))  # (out_channels, in_channels, height, width)
    # Horizontal line detector
    filters[0, 0] = np.array([[1, 1], [0, 0]])
    # Vertical line detector
    filters[1, 0] = np.array([[1, 0], [1, 0]])
    
    # Apply general convolution with dilation
    general_result = conv2d_general(
        batch_input, 
        filters,
        stride=(1, 1),
        padding=(0, 0),
        dilation=(2, 2)  # Dilated convolution
    )
    
    print("\nGeneral convolution result:")
    print("Output shape:", general_result.shape)
    print("Image 1, Horizontal detector:\n", general_result[0, 0])
    print("Image 1, Vertical detector:\n", general_result[0, 1])
    print("Image 2, Horizontal detector:\n", general_result[1, 0])
    print("Image 2, Vertical detector:\n", general_result[1, 1])
    
    print("\nNote: With dilation=2, we're skipping pixels in the kernel pattern,")
    print("which increases the receptive field without adding parameters.")
