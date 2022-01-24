import pytest
from colour_to_dmc.image import check_size_and_quantize


def test_check_size_and_quantize_small_size():
    #input_image = 'flowers.png'  # Image size: 225x225 pixels
    input_image = 'flowers.png'  # Image size: 225x225 pixels
    colour_limit = 255

    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The provided image is too small.'


