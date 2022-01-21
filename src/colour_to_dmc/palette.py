import cv2
import numpy as np
from collections import Counter
from colours import rgb_to_dmc, dmc_threads


# class Palette:
#     pass

def closest_unique_dmc_threads(image):
    # flatten the array by concatenating the lists:
    bgr_concat_array = np.concatenate(image, axis=0)
    # return unique B, G, R colour combination of a read_quantized_color_image by:
    # 1. turn lists into tuples
    # 2. use the unique() function to find the unique elements of an array.
    bgr_tuple_array = [tuple(row) for row in bgr_concat_array]
    unique_bgr_array = np.unique(bgr_tuple_array, axis=0)

    # find the closest dmc colour using unique bgr values
    closest_dmc_threads = [(rgb_to_dmc(c[2], c[1], c[0])) for c in unique_bgr_array]
    # dedupe the result
    unique_dmc_threads = [dict(t) for t in {tuple(d.items()) for d in closest_dmc_threads}]
    print("Total unique DMC threads found: ", len(unique_dmc_threads))
    return unique_dmc_threads


def generate_thread_palette(dmc_threads_found, percent_limit, image):
    # get a list of all thread occurrences from the closest_dmc_colours
    thread_occurrences = [thread_nr['floss'] for thread_nr in dmc_threads_found] # closest_dmc_threads
    print(thread_occurrences)
    # count thread occurrences found
    thread_counts = Counter(thread_occurrences)
    #print(thread_counts)
    # calculate the percentage use for each thread, save into a list of tuples. e.g.:[('#3371', 1.3157894736842104)]
    thread_percentages = [
        (i, thread_counts[i] / len(dmc_threads_found) * 100.0)
        for i in thread_counts]

    #print("thread_percentages", thread_percentages)

    #limit_low_occurring_threads = percent_limit
    filtered_thread_list = [
        thread for thread in thread_percentages if thread[1] > percent_limit]

    print("filtered_thread_list", len(filtered_thread_list))

    filtered_thread_list.sort(key=lambda x: x[1], reverse=True)
    filtered_thread_list_50 = filtered_thread_list[0:50]
    print("filtered_thread_list_50", len(filtered_thread_list_50))
    h, _, _ = image.shape
    size = 0

    filtered_thread_list_to_print = []

    if filtered_thread_list_50:
        # print(filtered_thread_list_50)
        size += int(h / len(filtered_thread_list_50))
        filtered_thread_list_to_print.extend(filtered_thread_list_50)
    else:
        try:
            size += int(h / len(filtered_thread_list)) # ZeroDivisionError: division by zero by  python cli.py roses.jpeg -p 2 -c 255
            filtered_thread_list_to_print.extend(filtered_thread_list)
        except ZeroDivisionError:
            print("A ZeroDivisionError occurred.")


    dmc_thread_dict = {dmc_thread['floss']: dmc_thread for dmc_thread in dmc_threads}  # csv data saved to dict
    for idx, color in enumerate(filtered_thread_list_to_print):
        b, g, r = (
            dmc_thread_dict[color[0]]["blue"],
            dmc_thread_dict[color[0]]["green"],
            dmc_thread_dict[color[0]]["red"]
        )

        cv2.rectangle(
            # thickness: It is the thickness of the rectangle borderline in px.
            # Thickness of -1 px will fill the rectangle shape by the specified color.
            image, (0, size * idx), (size * 2, (size * idx) + size), (b, g, r), -1)

        cv2.putText(
            image,
            dmc_thread_dict[color[0]]["floss"],
            (0, size * idx + (int(size / 2))),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255 - b, 255 - g, 255 - r),
            1,
        )


