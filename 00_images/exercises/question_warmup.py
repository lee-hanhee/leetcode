# 🧪 Practice Question: Subimage Localization via Sliding Convolution
# Problem Statement:
# You are given:
# A grayscale main image main_img of shape (H, W)
# A grayscale subimage template_img of shape (h, w), where h ≤ H and w ≤ W
# Your task is to:
# Implement a manual sliding window mechanism that extracts all (h, w)-sized patches from main_img.
# For each patch, compute the Normalized Cross-Correlation (NCC) between the patch and template_img as a similarity score.
# Construct a heatmap of similarity scores.
# Identify and return the coordinates (y, x) in main_img where the highest similarity occurs — i.e., most likely location of the subimage.
# Visualize the heatmap using Matplotlib and draw a bounding box around the detected subimage.
# Re-import necessary libraries after code execution state reset
import numpy as np
import matplotlib.pyplot as plt

def find_subimage_location(main_img, template_img):
    """
    Parameters:
        main_img: 2D np.ndarray of shape (H, W) representing the main grayscale image
        template_img: 2D np.ndarray of shape (h, w) representing the subimage

    Returns:
        heatmap: 2D np.ndarray of similarity scores
        top_left: Tuple[int, int] — coordinates (y, x) where the template best matches
    """
    H, W = main_img.shape
    h, w = template_img.shape

    heatmap = np.zeros((H - h + 1, W - w + 1))
    template_mean = np.mean(template_img)
    template_std = np.std(template_img)
    
    for i in range(H - h + 1):
        for j in range(W - w + 1):
            subimage = main_img[i:i+h, j:j+w]
            sub_mean = np.mean(subimage)
            sub_std = np.std(subimage)

            if sub_std != 0 and template_std != 0:
                ncc = np.sum((subimage - sub_mean) * (template_img - template_mean)) / (h * w * sub_std * template_std)
            else:
                ncc = 0  # avoid divide by zero

            heatmap[i, j] = ncc

    max_idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
    return heatmap, max_idx

# Demo with synthetic data
main_img = np.random.rand(20, 20)
template_img = main_img[8:13, 8:13]

heatmap, top_left = find_subimage_location(main_img, template_img)

# Visualization with bounding box
plt.figure(figsize=(6, 5))
plt.imshow(heatmap, cmap='hot')
plt.colorbar()
plt.title(f"Best match at {top_left}")
plt.show()