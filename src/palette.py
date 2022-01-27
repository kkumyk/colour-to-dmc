import cv2
import numpy as np
from collections import Counter
from nearest_dmc_thread import rgb_to_dmc, dmc_threads


def find_and_filter_dmc_threads(image):
    """
    :param image: quantized image
    :return: a list of tuples with the thread number and its percent value of use
    [('#938', 7.0588235294117645), ('#814', 2.7450980392156863)]

    The function does the following calculations:
    1. it returns unique B, G, R colour combination of the quantized image and de-dupes them
    2. finds the closest DMC threads using unique BRG combinations and de-dupes them
    3. gets the list of all thread occurrences from the closest DMC threads list
    prior de-duplication and count them per thread
    4. calculate the percentage use for each thread
    5. returns a list of tuples for each thread number/percentage combination e.g.:[('#3371', 1.3157894736842104)]
    """

    # flatten the array by concatenating the lists:
    bgr_concat_array = np.concatenate(image, axis=0)
    # return unique B, G, R colour combination of a quantized image by:
    # 1. turning lists into tuples
    # 2. using the unique() function to find the unique elements of an array.
    bgr_tuple_array = [tuple(row) for row in bgr_concat_array]
    unique_bgr_array = np.unique(bgr_tuple_array, axis=0)

    # find the closest dmc threads using unique bgr values == up to specified number of colours in the quantised image.
    closest_dmc_threads = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array]
    print("Total DMC thread matches found:", len(closest_dmc_threads))

    # dedupe the result
    unique_dmc_threads = [dict(t) for t in {tuple(d.items()) for d in closest_dmc_threads}]
    print("Total unique DMC threads: ", len(unique_dmc_threads))

    # get a list of all thread occurrences from the closest_dmc_colours
    thread_occurrences = [thread_nr['thread'] for thread_nr in closest_dmc_threads]
    # count thread occurrences found
    thread_counts = Counter(thread_occurrences)

    # calculate the percentage use for each thread, save into a list of tuples. e.g.:[('#3371', 1.3157894736842104)]
    thread_percentages = [
        (i, thread_counts[i] / len(closest_dmc_threads) * 100.0)
        for i in thread_counts]

    return thread_percentages


def generate_thread_palette(thread_percentages, percent_limit):
    """
    :param thread_percentages: a list of tuples returned from closest_unique_dmc_threads function
    :param percent_limit: a percent number supplied by the used from the CLI which is used
    to filter out DMC threads lower than that; the default is set to 1.
    :return: a filtered list of tuples for each thread number/percentage combination baced on the
    percent_limit specified by the user.
    """

    filtered_thread_list = [thread for thread in thread_percentages if thread[1] > percent_limit]
    # sort threads by percent value
    filtered_thread_list.sort(key=lambda x: x[1], reverse=True)
    print("Filtered DMC threads to print:", len(filtered_thread_list))

    filtered_thread_list_to_print = []

    if len(filtered_thread_list) > 50:
        filtered_thread_list_50 = filtered_thread_list[0:50]
        print("Number of DMC threads to print:", len(filtered_thread_list_50))
        filtered_thread_list_to_print.extend(filtered_thread_list_50)
    else:
        filtered_thread_list_to_print.extend(filtered_thread_list)

    return filtered_thread_list_to_print


def print_thread_palette(threads_to_print, image):
    """
    :param threads_to_print: list of tuples - output from the generate_thread_palette function
    :param image: quantized image
    :return: an image with the thread palette printed onto it.
    """

    dmc_thread_dict = {dmc_thread['thread']: dmc_thread for dmc_thread in dmc_threads}

    for idx, colour in enumerate(threads_to_print):
        b, g, r = (
            dmc_thread_dict[colour[0]]["blue"],
            dmc_thread_dict[colour[0]]["green"],
            dmc_thread_dict[colour[0]]["red"]
        )

        h, _, _ = image.shape
        size = int(h / len(threads_to_print))

        cv2.rectangle(
            # thickness of -1 px will fill the rectangle shape by the specified colour.
            image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

        cv2.putText(
            image,
            dmc_thread_dict[colour[0]]["thread"],
            (0, size * idx + (int(size / 2))),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255 - b, 255 - g, 255 - r),
            1,
        )
    return image
