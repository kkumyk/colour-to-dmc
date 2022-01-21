import sys
from PIL import Image


def check_size_and_quantize(input_image, colour_limit):
    """
    Check the size of the provided image and exits the program if not satisfied.
    Else, quantizes the image.
    """
    image_to_quantize = Image.open(input_image)
    width, height = image_to_quantize.size

    if width < 1000 or height < 1100:
        print("Please provide an image with a width of at least 1107px and a height of at least 1250px.")
        sys.exit("The provided image is too small.")
    else:
        quantized_image = image_to_quantize.quantize(colour_limit)
    return quantized_image

