import pytest
from colour_to_dmc.image import check_size_and_quantize


@pytest.mark.parametrize("expected_exception, input_image, colour_limit",
                         [(SystemExit, 'yellow-flower.jpeg', 255),
                          (SystemExit, 'irises.jpeg', 255)])
def test_check_size_and_quantize_incorrect_size(expected_exception, input_image, colour_limit):
    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The provided image is too small.'

#
# @pytest.mark.parametrize("input_image, colour_limit, expected_result",
#                          [('roses.jpeg', 255, 'JPEG'),
#                           ('Jan_Frans_van_Dael.jpg', 255, 'JPEG')
#                           ])
# def test_check_size_and_quantize_correct_format(input_image, colour_limit, expected_result):
#     assert check_size_and_quantize(input_image, colour_limit) == expected_result
