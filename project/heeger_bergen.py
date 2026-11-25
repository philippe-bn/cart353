# Adapted from: Implementation of the Heeger and Bergen texture synthesis algorithm. 2024 https://visionbook.mit.edu/textures.html

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, transform
from skimage.color import rgb2gray, rgba2rgb
from skimage.exposure import match_histograms
import pyrtools as pt

def load_image(image_path, count):
    img = io.imread(image_path)
    if (count == 0):
        return rgb2gray(img)
    else:
        img_rgb = rgba2rgb(img)
        return rgb2gray(img_rgb)
    

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

def execute(count):
    #Load an example texture
    # sample_image = load_image('http://people.csail.mit.edu/torralba/share/course/triangle.jpg')
    # sample_image = load_image('https://i0.wp.com/picjumbo.com/wp-content/uploads/realistic-concrete-wall-texture-free-photo.jpg?w=2210&quality=70')

    # sample_image = load_image('realistic-concrete-wall-texture-free-photo.webp')
    # sample_image = load_image('concrete-2316571_1280.jpg')
    # sample_image = load_image('istockphoto-481248302-612x612.jpg')
    if (count == 0):
        sample_image = load_image('close-up-rough-speckled-concrete-texture-featuring-irregular-grainy-pattern-ideal-backgrounds-design-textures-360187777.webp', count)
    else:
        sample_image = load_image(f'static/uploads/synthesized_{count-1}.png', count)

    sample_image = transform.resize(sample_image, (256, 256))

    Niterations = 10 # 10 with basic size is 2.5 seconds, 100 is 10 seconds (so 4x longer)
    synthesized = synthesis(sample_image, Niterations)

    # Display results
    # plt.figure(figsize=(12, 6))
    # plt.subplot(1, 2, 1)
    # plt.title('Original Texture')
    # plt.imshow(sample_image, cmap='gray')
    # plt.axis('off')

    # plt.subplot(1, 2, 2)
    # plt.title('Synthesized Texture')
    # plt.imshow(synthesized, cmap='gray')
    # plt.axis('off')
    # plt.show()

    plt.imsave(f'static/uploads/synthesized_{count}.png', synthesized, cmap='gray')
    return