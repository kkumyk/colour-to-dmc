import cv2
import pandas as pd
import numpy as np
from colours import rgb_to_dmc, dmc_colors
from collections import Counter
import matplotlib.pyplot as plt

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
dmc_colours = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array] # RENAME the variable

# dedupe colour_list
unique_dmc_colours = [dict(t) for t in {tuple(d.items()) for d in dmc_colours}]

# get a list of all floss/thread occurrences from the dmc_colours
floss_seq = [x['floss'] for x in dmc_colours]

# https://docs.python.org/3/library/collections.html#collections.Counter
# count floss occurrences found
floss_counts = Counter(floss_seq)

# calculate the use percentage of each floss
floss_use_percentage = [
    (i, floss_counts[i] / len(dmc_colours) * 100.0)
    for i in floss_counts]

limit_low_occurring_threads = 2  # %
filtered_floss_list = [
    color for color in floss_use_percentage if color[1] > limit_low_occurring_threads
]
print('Number of most used threads: ', len(filtered_floss_list))

filtered_floss_df = pd.DataFrame(filtered_floss_list).rename(columns={0: 'floss', 1: '%'})

unique_dmc_df = pd.DataFrame(unique_dmc_colours)
# unique_dmc_df[["floss", "description"]]

merged_colours = pd.merge(filtered_floss_df, unique_dmc_df, how="left", on="floss").sort_values('%', ascending=False)
dmc_palette = merged_colours[["floss", "description", "red", "green", "blue", "%"]]


print("DMC Palette", dmc_palette)

# get the list of rgb combinations for each
# http://net-informations.com/ds/pd/iterate.htm
rgb_palette = [[x, y, z] for x, y, z in zip(dmc_palette['red'], dmc_palette['green'], dmc_palette['blue'])]

plt.imshow([rgb_palette])
# plt.show()

# overlay the color palette on top of the image
_, w, _ = image.shape
size = int(w / len(filtered_floss_list))
y = size

#
# print("DMC COLORS", dmc_colors)
#
# for idx, color in enumerate(filtered_floss_list):
#     b, g, r = (
#         dmc_colors[color[0]]["blue"],
#         dmc_colors[color[0]]["green"],
#         dmc_colors[color[0]]["red"],
#     )
#     cv2.rectangle(
#         image, (size * idx, 0), ((size * idx) + size, size), (b, g, r), -1
#     )
#
#
# print('Size: ', size)
#
# print('Image width: ', w)
#
# cv2.rectangle(image,(384,0),(510,128),(0,255,0),3)

