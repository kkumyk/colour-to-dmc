import sys
from PIL import Image


def check_size_and_quantize(input_image, colour_limit):
    """
    Checks the image type and the size of the provided image and exits the program if:
    - the image is not in PNG or JPEG formats
    - width < 1000px or height < 1100px.
    Else, it quantizes the image.
    """
    if colour_limit < 1:
        print("Please choose the number of colours to use in the image. It should between 1 and 255.")
        sys.exit("The given number is too small.")

    elif colour_limit > 255:
        print("Please choose the number of colours to use in the image. It should between 1 and 255.")
        sys.exit("The given number is too large.")

    else:

        image_to_quantize = Image.open(input_image)
        file_format = image_to_quantize.format

        if file_format == 'JPEG' or file_format == 'PNG':
            width, height = image_to_quantize.size

            if width < 1000 or height < 1100:
                print("Please provide an image with a width of at least 1000px and a height of at least 1100px.")
                sys.exit("The provided image is too small.")

            else:
                quantized_image = image_to_quantize.quantize(colour_limit)
            return quantized_image

        else:
            print("Please provide a valid image in one of the following formats: PNG or JPEG.")
            sys.exit("The provided image should be in PNG or JPEG format.")
