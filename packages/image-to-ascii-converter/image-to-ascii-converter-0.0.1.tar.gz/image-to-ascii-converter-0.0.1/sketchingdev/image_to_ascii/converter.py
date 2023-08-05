from PIL import Image

from sketchingdev.image_to_ascii.centre import centre_in_container

GREYSCALE_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', ',', '.', ' ']
GREYSCALE_CHARS_MAX_INDEX = len(GREYSCALE_CHARS) - 1
ELEMENT_RANGE = element_range = GREYSCALE_CHARS_MAX_INDEX / 255

# PIL Modes
EIGHT_BIT_BLACK_AND_WHITE = "L"
EIGHT_BIT_BLACK_AND_WHITE_WITH_ALPHA = "LA"
EIGHT_BIT_OTHER_COLOUR_PALETTE = "P"


def map_pixel_to_character(pixel):
    char_index = int(ELEMENT_RANGE * pixel)
    return GREYSCALE_CHARS[char_index]


def convert_to_rgb(image, alpha_colour=(255, 255, 255)):
    """
    :param image: Image to be converted
    :param alpha_colour: Colour used in place of transparent pixels
    :return: Image that has been converted to an RGB mode
    """
    if image.format == "PNG" and image.mode == "RGBA":
        background = Image.new("RGBA", image.size, alpha_colour)
        background.paste(image, image)
        return background.convert("RGB")

    if image.mode in [EIGHT_BIT_OTHER_COLOUR_PALETTE, EIGHT_BIT_BLACK_AND_WHITE_WITH_ALPHA]:
        image = image.convert("RGBA")
        background = Image.new("RGBA", image.size, alpha_colour)
        background.paste(image, image)
        return background.convert("RGB")

    if image.mode != "RGB":
        return image.convert("RGB")

    return image


def convert_to_greyscale(image):
    return image.convert(EIGHT_BIT_BLACK_AND_WHITE)


def convert_image_to_ascii(image):
    image = convert_to_rgb(image)
    image = convert_to_greyscale(image)

    width, height = image.size
    pixels = list(image.getdata())
    rows = [pixels[i * width:(i + 1) * width] for i in range(height)]

    ascii_rows = []
    for row in rows:
        textual_row = "".join([map_pixel_to_character(pixel) for pixel in row])

        ascii_rows.append(textual_row)

    return ascii_rows


def format_image(size, image_path):
    """
    :param size: Size of the ASCII image to generate
    :param image_path: A filename (string), pathlib.Path object or a file object.
       The file object must implement :py:meth:`~file.read`,
       :py:meth:`~file.seek`, and :py:meth:`~file.tell` methods,
       and be opened in binary mode.
    :returns: ASCII representation of the image
    :exception IOError: If the file cannot be found, or the image cannot be
       opened and identified.
    """
    with Image.open(image_path) as image:
        image.thumbnail(size, Image.ANTIALIAS)
        ascii_lines = convert_image_to_ascii(image)

    centred_image = centre_in_container(ascii_lines, size)
    return "\n".join(centred_image).rstrip("\n")
