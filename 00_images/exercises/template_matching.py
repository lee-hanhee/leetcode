import matplotlib.pyplot as plt
import numpy as np

def template_match(main_image, template):
    """
    Slides a template over a larger image and computes the normalized cross-correlation (NCC).

    Parameters:
        main_image (np.ndarray): 2D grayscale image.
        template (np.ndarray): 2D grayscale template image.

    Returns:
        np.ndarray: Heatmap of similarity scores.
    """
    h, w = main_image.shape
    th, tw = template.shape
    heatmap = np.zeros((h - th + 1, w - tw + 1))

    template_mean = np.mean(template)
    template_std = np.std(template)

    for i in range(h - th + 1):
        for j in range(w - tw + 1):
            patch = main_image[i:i+th, j:j+tw]
            patch_mean = np.mean(patch)
            patch_std = np.std(patch)
            if patch_std != 0:
                ncc = np.sum((patch - patch_mean) * (template - template_mean)) / (th * tw * patch_std * template_std)
                heatmap[i, j] = ncc
    
    return heatmap

def generate_heatmap(heatmap):
    """
    Displays a heatmap using matplotlib.

    Parameters:
        heatmap (np.ndarray): 2D array of similarity scores.

    Returns:
        None
    """
    plt.figure(figsize=(6, 5))
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title("Heatmap of Similarity Scores")
    plt.show()
