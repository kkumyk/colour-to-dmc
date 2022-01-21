import argparse
import cv2
from image import check_size_and_quantize
from palette import closest_dmc_colours, generate_thread_palette

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

reduced_colour_image = check_size_and_quantize(args.input, args.colours)

reduced_colour_image.save('reduced_colour_image.png')
reduced_colour_image = cv2.imread('reduced_colour_image.png')

unique_closest_dmc_colours = closest_dmc_colours(reduced_colour_image)
thread_palette = generate_thread_palette(unique_closest_dmc_colours, args.percent, reduced_colour_image, args.output)

