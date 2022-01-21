import sys
import cv2
from PIL import Image
from cli import input_image, colour_limit


def check_and_quantize():
    image_to_quantize = Image.open(input_image)
    width, height = image_to_quantize.size

    if width < 1000 or height < 1100:
        print("Please provide an image with a width of at least 1107px and a height of at least 1250px.")
        sys.exit("The provided image is too small.")
    else:
        quantized_image = image_to_quantize.quantize(colour_limit)
        quantized_image.save('reduced_colour_image.png')
        reduced_colour_image = cv2.imread('reduced_colour_image.png')
