import cv2
import numpy as np
from colours import rgb_to_dmc

# returns a nested array of lists with B, G, R colours present in an image
image = cv2.imread('flowers.png')

# we can access this colour combination by x,y position
# b, g, r = image[80,160]
# print(b, g, r)

# flatten the array by concatenating the lists:
bgr_concat_array = np.concatenate(image, axis=0)

# return unique B, G, R colour combination of an image by:
# 1. turning lists into tuples and
# 2. using the unique() function to find the unique elements of an array.

bgr_tuple_array = [tuple(row) for row in bgr_concat_array]
unique_bgr_array = np.unique(bgr_tuple_array, axis=0)

# find the closest dmc colour using unique bgr values in the unique_bgr_array
dmc_colours = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array]

# dedupe colour_list
unique_dmc_colours = [dict(t) for t in {tuple(d.items()) for d in dmc_colours}] 

# get a list of all floss/thread occurrences from the dmc_colours
seq = [x['floss'] for x in dmc_colours]
print(seq)


