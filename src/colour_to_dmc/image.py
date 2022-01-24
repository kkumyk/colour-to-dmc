import sys
from PIL import Image


def check_size_and_quantize(input_image, colour_limit):
    """
    Checks the size of the provided image and exits the program if
    width < 1000px or height < 1100px. Else, quantizes the image.
    """
    image_to_quantize = Image.open(input_image)
    width, height = image_to_quantize.size

    if width < 1000 or height < 1100:
        print("Please provide an image with a width of at least 1000px and a height of at least 1100px.")
        sys.exit("The provided image is too small.")

    else:
        # add check for colour_limit
        quantized_image = image_to_quantize.quantize(colour_limit)

    return quantized_image
