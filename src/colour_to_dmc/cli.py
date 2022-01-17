import argparse, image

parser = argparse.ArgumentParser(
    description="Get a DMC colour palette for an image."
)
parser.add_argument("input", help="an input file")
parser.add_argument(
    "-o", "--output",
    default='palette.jpg',
    help="an output file",
    required=False
)
parser.add_argument(
    "-d", "--div",
    type=int,
    default=64,
    required=False
)

args = parser.parse_args()

input_image = args.input
output_image = args.output
div = args.div


