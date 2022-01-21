import argparse
import cv2
import os
from image import check_size_and_quantize
from palette import closest_unique_dmc_threads, generate_thread_palette

parser = argparse.ArgumentParser(description="Get a DMC colour palette for an image.")

parser.add_argument("input", help="an input file")

parser.add_argument(
    "-o", "--output",
    default='palette.jpg',
    help="an output file",
    required=False
)

parser.add_argument(
    "-p", "--percent",
    type=int,
    default=1,
    help="percent number to use for filtering identified colours",
    required=False
)

# provide number of colours as an argument
parser.add_argument(
    "-c", "--colours",
    type=int,
    default=255,
    help="a number to use to reduce the image to the specified nr of colours",
    required=False
)

args = parser.parse_args()

image_to_quantize = check_size_and_quantize(args.input, args.colours)
image_to_quantize.save('reduced_colour_image.png')
reduced_colour_image = cv2.imread('reduced_colour_image.png')

dmc_threads_found = closest_unique_dmc_threads(reduced_colour_image)
thread_palette = generate_thread_palette(dmc_threads_found, args.percent, reduced_colour_image)

cv2.imwrite(args.output, reduced_colour_image)
# delete reduced colour image from the folder
os.remove('reduced_colour_image.png')
