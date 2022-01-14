import cv2
import pandas as pd
import numpy as np

from colours import rgb_to_dmc, dmc_colors
from collections import Counter

# returns a nested array of lists with B, G, R colours present in an image
original_image = cv2.imread('roses.jpeg')

# reduce image colours
div = 64
quantized_image = original_image // div * div + div // 2
cv2.imwrite('quantized_image.jpg', quantized_image)


def get_scaled_down_image(image):
    MAXWIDTH, MAXHEIGHT = 400, 400
    w = MAXWIDTH / image.shape[1]
    h = MAXHEIGHT / image.shape[0]
    scale = min(w, h)
    dim = (int(image.shape[1] * scale), int(image.shape[0] * scale))
    return cv2.resize(image, dim)

# scale down the original and the quantized images
scaled_down_image = get_scaled_down_image(original_image)
scaled_down_quantized_image = get_scaled_down_image(quantized_image)
# we can access this colour combination by x,y position
# b, g, r = image[80,160]
# print(b, g, r)
# flatten the array by concatenating the lists:
bgr_concat_array = np.concatenate(scaled_down_image, axis=0)
bgr_concat_quantized_array = np.concatenate(scaled_down_quantized_image, axis=0)

# return unique B, G, R colour combination of a scaled_down_image by:
# 1. turning lists into tuples and
# 2. using the unique() function to find the unique elements of an array.

bgr_tuple_array = [tuple(row) for row in bgr_concat_array]
unique_bgr_array = np.unique(bgr_tuple_array, axis=0)

# find the closest dmc colour using unique bgr values in the unique_bgr_array
dmc_colours = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array]  # RENAME the variable
print("DMC_COLOURS", dmc_colours)
# dedupe colour_list
unique_dmc_colours = [dict(t) for t in {tuple(d.items()) for d in dmc_colours}]

# get a list of all floss/thread occurrences from the dmc_colours
floss_seq = [x['floss'] for x in dmc_colours]

# https://docs.python.org/3/library/collections.html#collections.Counter
# count floss occurrences found
floss_counts = Counter(floss_seq)
print("TOTAL NUMBER OF FLOSS THREADS FOUND: ", len(floss_counts))
# calculate the use percentage of each floss
floss_use_percentage = [
    (i, floss_counts[i] / len(dmc_colours) * 100.0)
    for i in floss_counts]

limit_low_occurring_threads = 1  # %
filtered_floss_list = [
    color for color in floss_use_percentage if color[1] > limit_low_occurring_threads]

print("NOT_SORTED_filtered_floss_list", filtered_floss_list)

# filtered_floss_list_first = filtered_floss_list.sort(key=lambda x:x[0])
# print("filtered_floss_list_first", filtered_floss_list_first)

# https://www.kite.com/python/answers/how-to-sort-a-list-of-tuples-by-the-second-value-in-python
filtered_floss_list.sort(key=lambda x: x[1])

filtered_floss_df = pd.DataFrame(filtered_floss_list).rename(columns={0: 'floss', 1: '%'})
unique_dmc_df = pd.DataFrame(unique_dmc_colours)
merged_colours = pd.merge(filtered_floss_df, unique_dmc_df, how="left", on="floss").sort_values('%', ascending=False)

dmc_palette = merged_colours[["floss", "description", "red", "green", "blue", "%", "dmc_row", "cat-1", "cat-2"]]
dmc_palette_dmc_row = dmc_palette.sort_values(by=['dmc_row'])
print(dmc_palette_dmc_row)

sorted_floss = dmc_palette_dmc_row['floss'].to_list()

# get the list of rgb combinations for each
# http://net-informations.com/ds/pd/iterate.htm
# rgb_palette = [[x, y, z] for x, y, z in zip(dmc_palette['red'], dmc_palette['green'], dmc_palette['blue'])]

rgb_palette = [[x, y, z] for x, y, z in
               zip(dmc_palette_dmc_row['red'], dmc_palette_dmc_row['green'], dmc_palette_dmc_row['blue'])]

print("RGB-PALETTE", rgb_palette)
# overlay the color palette on top of the original image
# _, w, _ = original_image.shape
# size = int(w / len(filtered_floss_list))

h, _, _ = original_image.shape
size = int(h / len(filtered_floss_list))
y = size
# print("Y IS: ", y)
# print("DMC COLORS", dmc_colors)
print("FILTERED FLOSS LIST", filtered_floss_list)
print("sorted_floss", sorted_floss)

sorted_filtered_floss_list = sorted(filtered_floss_list, key=lambda item: sorted_floss.index(item[0]))

test_dmc_thread_dict = {dmc_color['floss']: dmc_color for dmc_color in dmc_colors}  # csv data saved to dict

for idx, color in enumerate(sorted_filtered_floss_list):
    b, g, r = (
        test_dmc_thread_dict[color[0]]["blue"],
        test_dmc_thread_dict[color[0]]["green"],
        test_dmc_thread_dict[color[0]]["red"]
    )

    # print(color[0], r, g, b)
    cv2.rectangle(
        # thickness: It is the thickness of the rectangle border line in px. Thickness of -1 px will fill the rectangle shape by the specified color.
        # original_image, (size * idx, 0), ((size * idx) + size, size), (b, g, r), -1)
        original_image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

    cv2.putText(
        original_image,
        test_dmc_thread_dict[color[0]]["floss"],
        (0, size * idx + (int(size / 2))),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255 - b, 255 - g, 255 - r),
        1,
    )

cv2.imwrite('palette.jpg', original_image)

dmc_palette_new = dmc_palette_dmc_row.copy()
dmc_palette_new.drop(['%', 'dmc_row'], axis=1, inplace=True)
dmc_palette_new['sum'] = (dmc_palette_new.sum(axis=1)) / 3

# dmc_palette_new.sort_values("sum", inplace=True)
dmc_palette_new.sort_values(['sum'], ascending=[True], inplace=True)

average_pos_floss = dmc_palette_new['floss'].to_list()
print(average_pos_floss)

average_sorted_floss = sorted(filtered_floss_list, key=lambda item: average_pos_floss.index(item[0]))
print(average_sorted_floss)

for idx, color in enumerate(average_sorted_floss):
    b, g, r = (
        test_dmc_thread_dict[color[0]]["blue"],
        test_dmc_thread_dict[color[0]]["green"],
        test_dmc_thread_dict[color[0]]["red"]
    )

    # print(color[0], r, g, b)
    cv2.rectangle(
        original_image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

    cv2.putText(
        original_image,
        test_dmc_thread_dict[color[0]]["floss"],
        (0, size * idx + (int(size / 2))),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255 - b, 255 - g, 255 - r),
        1,
    )

cv2.imwrite('average_position_palette.jpg', original_image)


# Task: get the closest colour alternative from the unique colours.


def closest(colors, color):
    # filtered = [i for i in colors if i != color]
    # filtered = np.array(filtered)
    filtered = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((filtered - color) ** 2, axis=1))
    # print("DISTANCES", distances)
    index_of_smallest = np.where(distances == np.amin(distances))
    # print("INDEX OF SMALLEST", index_of_smallest)
    smallest_distance = filtered[index_of_smallest]
    # print("SMALLEST INDEX", smallest_distance)
    return smallest_distance


closest_color = closest(rgb_palette, [135, 125, 115])
print("TEST", closest_color)

# nearest_colours_dict = {}
# for c in rgb_palette:
#     nearest_colours.append(closest(rgb_palette, c))


nearest_colours = []
for c in rgb_palette:
    nearest_colours.append(closest(rgb_palette, c))




flat_nearest_colours = [item for sublist in nearest_colours for item in sublist]
print("NEAREST COLOURS", flat_nearest_colours)



# print("PALETTE", rgb_palette)
nearest_colours_df = pd.DataFrame(flat_nearest_colours, columns=['red', 'green', 'blue'])
print(nearest_colours_df)

print("UNIQUE DMC_COLOURS", unique_dmc_colours)
unique_dmc_colours_df = pd.DataFrame.from_dict(unique_dmc_colours, orient='columns')

unique_dmc_colours_df = unique_dmc_colours_df.iloc[:, :-4]
unique_dmc_colours_df.drop('index', axis=1, inplace=True)

# unique_dmc_colours_df.drop_duplicates(['floss', 'description'], keep= 'first')
# #print(unique_dmc_colours_df)

df_merge = pd.merge(nearest_colours_df, unique_dmc_colours_df, on=['red','green','blue'], how='left')

df_merge = df_merge.iloc[:, 3:]
print(df_merge)
records = df_merge.to_records(index=False)
print(records)

#
# print(average_sorted_floss)

for idx, color in enumerate(records):
    b, g, r = (
        test_dmc_thread_dict[color[0]]["blue"],
        test_dmc_thread_dict[color[0]]["green"],
        test_dmc_thread_dict[color[0]]["red"]
    )

    # print(color[0], r, g, b)
    cv2.rectangle(
        original_image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

    cv2.putText(
        original_image,
        test_dmc_thread_dict[color[0]]["floss"],
        (0, size * idx + (int(size / 2))),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255 - b, 255 - g, 255 - r),
        1,
    )

cv2.imwrite('nearest_colour_test_palette.jpg', original_image)





#  https://stackoverflow.com/questions/3565108/which-is-most-accurate-way-to-distinguish-one-of-8-colors/3565191#3565191
#  https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors
#  https://i0.wp.com/lordlibidan.com/wp-content/uploads/2021/11/DMCThreadshadecardwithnewcolors.png?ssl=1
