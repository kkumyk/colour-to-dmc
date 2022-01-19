import argparse, image

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
    "-n", "--number",
    type=int,
    default=255,
    help="a number to use to reduce the image to the specified nr of colours",
    required=False
)

args = parser.parse_args()
input_image = args.input
output_image = args.output
percent = args.percent
number = args.number

