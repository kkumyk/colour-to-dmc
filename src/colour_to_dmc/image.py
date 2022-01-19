import os
import sys
import cv2
import numpy as np
from colours import rgb_to_dmc, dmc_threads
from collections import Counter
from cli import input_image, output_image, percent, number
from PIL import Image

# get the image
image_to_quantize = Image.open(input_image)

# specify the image size to be given for the input
width, height = image_to_quantize.size

if width < 1000 or height < 1100:
    print("Please provide an image with a width of at least 1107px and a height of at least 1250px.")
    sys.exit("The provided image is too small.")
else:
    reduced_color = image_to_quantize.quantize(number)
    reduced_color.save('reduced_color.png')

    reduced_color_image = cv2.imread('reduced_color.png')
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
    # print("CLOSEST_DMC_COLOURS", len(closest_dmc_colours))
    # print("UNIQUE_CLOSEST_DMC_COLOURS", len(unique_closest_dmc_colours))

    # get a list of all thread occurrences from the closest_dmc_colours
    thread_occurrences = [x['floss'] for x in closest_dmc_colours]

    # https://docs.python.org/3/library/collections.html#collections.Counter
    # count thread occurrences found
    thread_counts = Counter(thread_occurrences)

    # calculate the percentage use for each thread, save into a list of tuples. e.g.:[('#3371', 1.3157894736842104)]
    thread_percentages = [
        (i, thread_counts[i] / len(closest_dmc_colours) * 100.0)
        for i in thread_counts]

    limit_low_occurring_threads = percent  # %

    filtered_thread_list = [
        thread for thread in thread_percentages if thread[1] > limit_low_occurring_threads]

    print("NOT-FILTERED", len(thread_percentages))
    print("FILTERED", len(filtered_thread_list))

    h, _, _ = reduced_color_image.shape
    size = int(h / len(filtered_thread_list))
    y = size
    # print("FILTERED FLOSS LIST", filtered_thread_list)

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
            reduced_color_image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

        cv2.putText(
            reduced_color_image,
            dmc_thread_dict[color[0]]["floss"],
            (0, size * idx + (int(size / 2))),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255 - b, 255 - g, 255 - r),
            1,
        )

        cv2.imwrite(output_image, reduced_color_image)

    # delete reduced colour image from the folder
    os.remove('reduced_color.png')
"""


3. algo to print out not more than 50 colours.

"""