from colour_to_dmc.image import check_size_and_quantize
import pytest


@pytest.mark.parametrize("expected_exception, input_image, colour_limit",
                         [(SystemExit, 'yellow-flower.jpeg', 255),
                          (SystemExit, 'irises.jpeg', 255)])
def test_check_size_and_quantize_small_size(expected_exception, input_image, colour_limit):
    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The provided image is too small.'


@pytest.mark.parametrize("input_image, colour_limit, expected_result",
                         [('Jan_Frans_van_Dael.jpg', 255, "<class 'PIL.Image.Image'>"),
                          ('roses.jpeg', 255, "<class 'PIL.Image.Image'>")])
def test_check_size_and_quantize_correct_size(input_image, colour_limit, expected_result):
    assert str(type(check_size_and_quantize(input_image, colour_limit))) == "<class 'PIL.Image.Image'>"


@pytest.mark.parametrize("expected_exception, input_image, colour_limit",
                         [(SystemExit, 'tulips.gif', 255)])
def test_check_size_and_quantize_incorrect_format(expected_exception, input_image, colour_limit):
    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The provided image should be in PNG or JPEG format.'


@pytest.mark.parametrize("expected_exception, input_image, colour_limit",
                         [(SystemExit, 'roses.jpeg', -5)])
def test_check_size_and_quantize_incorrect_format(expected_exception, input_image, colour_limit):
    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The given number is too small.'


@pytest.mark.parametrize("expected_exception, input_image, colour_limit",
                         [(SystemExit, 'roses.jpeg', 555)])
def test_check_size_and_quantize_incorrect_format(expected_exception, input_image, colour_limit):
    with pytest.raises(SystemExit) as e:
        check_size_and_quantize(input_image, colour_limit)
    assert e.type == SystemExit
    assert e.value.code == 'The given number is too large.'