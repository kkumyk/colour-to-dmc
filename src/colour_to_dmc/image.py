import cv2
import pandas as pd
import numpy as np

from colours import rgb_to_dmc, dmc_threads
from collections import Counter

# returns a nested array of lists with B, G, R colours present in an image
original_image = cv2.imread('roses.jpeg')


# original_image = cv2.imread('Mark-Liam-Smith-Scarab-Beetle-Oil-on-panel-2021-16x12.jpg')
# original_image = cv2.imread('Jan_Frans_van_Dael.jpg')

# https://stackoverflow.com/a/20715062
def quantize_image(image, div=32):
    """
    Reduces the number of distinct colors used in an image.
    """
    quantized = image // div * div + div // 2
    return quantized


# reduce the number of distinct colors in an image
# while preserving the color appearance of the image as much as possible
reduced_color_image = quantize_image(original_image)
# cv2.imwrite('quantized_image_test.jpg', reduced_color_image)

# we can access this colour combination by x,y position
# b, g, r = image[80,160]
# print(b, g, r)

# flatten the array by concatenating the lists:
bgr_concat_array = np.concatenate(reduced_color_image, axis=0)

# return unique B, G, R colour combination of a reduced_color_image by:
# 1. turn lists into tuples
# 2. use the unique() function to find the unique elements of an array.

bgr_tuple_array = [tuple(row) for row in bgr_concat_array]
unique_bgr_array = np.unique(bgr_tuple_array, axis=0)

# find the closest dmc colour using unique bgr values and dedupe the result
closest_dmc_colours = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array]
unique_closest_dmc_colours = [dict(t) for t in {tuple(d.items()) for d in closest_dmc_colours}]
print("CLOSEST_DMC_COLOURS", len(closest_dmc_colours))
print("UNIQUE_CLOSEST_DMC_COLOURS", len(unique_closest_dmc_colours))

# get a list of all thread occurrences from the closest_dmc_colours
thread_occurrences = [x['floss'] for x in closest_dmc_colours]

# https://docs.python.org/3/library/collections.html#collections.Counter
# count thread occurrences found
thread_counts = Counter(thread_occurrences)

# calculate the percentage use for each thread, save into a list of tuples. e.g.:[('#3371', 1.3157894736842104)]
thread_percentages = [
    (i, thread_counts[i] / len(closest_dmc_colours) * 100.0)
    for i in thread_counts]

limit_low_occurring_threads = 1  # %

filtered_thread_list = [
    thread for thread in thread_percentages if thread[1] > limit_low_occurring_threads]

print("NOT-FILTERED", len(thread_percentages))
print("FILTERED", len(filtered_thread_list))

h, _, _ = original_image.shape
size = int(h / len(filtered_thread_list))
y = size
print("FILTERED FLOSS LIST", filtered_thread_list)

dmc_thread_dict = {dmc_thread['floss']: dmc_thread for dmc_thread in dmc_threads}  # csv data saved to dict

for idx, color in enumerate(filtered_thread_list):
    b, g, r = (
        dmc_thread_dict[color[0]]["blue"],
        dmc_thread_dict[color[0]]["green"],
        dmc_thread_dict[color[0]]["red"]
    )

    # print(color[0], r, g, b)
    cv2.rectangle(
        # thickness: It is the thickness of the rectangle borderline in px.
        # Thickness of -1 px will fill the rectangle shape by the specified color.
        original_image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

    cv2.putText(
        original_image,
        dmc_thread_dict[color[0]]["floss"],
        (0, size * idx + (int(size / 2))),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255 - b, 255 - g, 255 - r),
        1,
    )

cv2.imwrite('palette.jpg', original_image)