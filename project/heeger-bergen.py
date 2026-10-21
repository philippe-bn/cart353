# Implementation of the Heeger and Bergen texture synthesis algorithm.
# 2024
#
# https://visionbook.mit.edu/textures.html

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, transform
from skimage.color import rgb2gray, rgba2rgb
from skimage.exposure import match_histograms

# pyrtools is a library used for image processing, particularly useful for operations involving pyramids and wavelets.
#pip install pyrtools
import pyrtools as pt

def load_image(image_path):
    img = io.imread(image_path)
    # img_rgb = rgba2rgb(img)
    # return rgb2gray(img_rgb)  # Convert to grayscale for simplicity
    return rgb2gray(img)  # Convert to grayscale for simplicity

def build_pyramid(image, max_levels): # this is not used, but nice to have it here for future reference
    return pt.pyramids.LaplacianPyramid(image, height=max_levels)

def build_steerable_pyramid(image, max_levels, orientations):
    return pt.pyramids.SteerablePyramidFreq(image, height=max_levels, order=orientations)

def histogram_matching(original, reference):
    matched = match_histograms(original, reference)
    return matched

def synthesis(input_texture, iterations=5, max_levels=3, orientations=6):
    original_pyramid = build_steerable_pyramid(input_texture, max_levels, orientations)
    synthesized_texture = np.random.rand(*input_texture.shape)

    for _ in range(iterations):
        # first match the histograms of the pixels distributions
        synthesized_texture = histogram_matching(synthesized_texture, input_texture)
        synth_pyramid = build_steerable_pyramid(synthesized_texture, max_levels, orientations)

        # Iterate through the scales and orientations of the pyramid. It is stored as a dictionary.
        for key, original_coeffs in original_pyramid.pyr_coeffs.items():
            synth_coeffs = synth_pyramid.pyr_coeffs[key]
            # Ensure both are numpy arrays for histogram matching
            matched = histogram_matching(synth_coeffs, original_coeffs)
            synth_pyramid.pyr_coeffs[key] = matched

        synthesized_texture = synth_pyramid.recon_pyr()

    synthesized_texture = histogram_matching(synthesized_texture, input_texture)
    return synthesized_texture

 #Load an example texture
# sample_image = load_image('http://people.csail.mit.edu/torralba/share/course/triangle.jpg')  # Replace with a valid URL or file path
# sample_image = load_image('https://i0.wp.com/picjumbo.com/wp-content/uploads/realistic-concrete-wall-texture-free-photo.jpg?w=2210&quality=70')  # Replace with a valid URL or file path
# sample_image = load_image('synthesized.png')  # Replace with a valid URL or file path
sample_image = load_image('realistic-concrete-wall-texture-free-photo.webp')  # Replace with a valid URL or file path

# sample_image = transform.resize(sample_image, (256, 256))  # Resize for simplicity
sample_image = transform.resize(sample_image, (1024, 1024))  # Resize for simplicity, testing higher resize

# plt.imshow(sample_image, cmap='gray')
# plt.show()
# Let's check the steerable pyramid decomposition of the sample image

# compute the pyramid with 2 scales and 4 orientations per scale:
original_pyramid = build_steerable_pyramid(sample_image, 2, 4)

# # the next function plots the output of all the filters
#pt.pyrshow(original_pyramid.pyr_coeffs)
Niterations = 10
synthesized = synthesis(sample_image, Niterations)
# Display results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Original Texture')
plt.imshow(sample_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Synthesized Texture')
plt.imshow(synthesized, cmap='gray')
plt.imsave('synthesized.png', synthesized)
plt.axis('off')

plt.show()