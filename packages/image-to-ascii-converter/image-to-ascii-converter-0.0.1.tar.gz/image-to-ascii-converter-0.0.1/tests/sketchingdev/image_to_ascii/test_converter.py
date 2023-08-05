import unittest

import ntpath
import os
from os import path
from parameterized import parameterized

from sketchingdev.image_to_ascii.converter import format_image


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def resolve_data_path(filename):
    data_dir = path.join(get_current_directory(), "data/")
    return path.join(data_dir, filename)


def read_test_file(file_path):
    full_path = resolve_data_path(file_path)
    with open(full_path, "r") as f:
        return f.read()


def custom_name_func(testcase_func, param_num, param):
    ascii_size = param.args[0]
    image_filename = ntpath.basename(param.args[1])

    return "%s_%s_of_%s" % (
        testcase_func.__name__,
        "%sx%s" % (ascii_size[0], ascii_size[1]),
        parameterized.to_safe_name(image_filename)
    )


class TestConsoleDisplayWithImages(unittest.TestCase):
    TEST_CASES = [
        ((10, 10),
         resolve_data_path("24bit-without-transparency.png"),
         resolve_data_path("24bit-without-transparency.png.10x10.txt")),
        ((10, 10),
         resolve_data_path("32bit-with-transparency.png"),
         resolve_data_path("32bit-with-transparency.png.txt")),
        ((12, 12),
         resolve_data_path("24bit-without-transparency.png"),
         resolve_data_path("24bit-without-transparency.png.12x12.txt")),
        ((10, 10),
         resolve_data_path("rgb-with-transparency.png"),
         resolve_data_path("rgb-with-transparency.png.10x10.txt")),
        ((20, 20),
         resolve_data_path("16bit-with-transparency.png"),
         resolve_data_path("16bit-with-transparency.png.20x20.txt")),
        ((1, 1),
         resolve_data_path("16bit-with-transparency.png"),
         resolve_data_path("16bit-with-transparency.png.1x1.txt")),
        ((10, 10),
         resolve_data_path("rgb-with-transparency.gif"),
         resolve_data_path("rgb-with-transparency.gif.10x10.txt")),
        ((10, 10),
         resolve_data_path("rgb.jpg"),
         resolve_data_path("rgb.jpg.10x10.txt")),
    ]

    @parameterized.expand(TEST_CASES, testcase_func_name=custom_name_func)
    def test_conversion(self, console_size, input_image, expected_ascii_output_file):
        ascii_output = format_image(console_size, input_image)

        expected_ascii_output = read_test_file(expected_ascii_output_file)
        self.assertEqual(expected_ascii_output, ascii_output)

    def generate_ascii_baseline_files(self):
        for test in self.TEST_CASES:
            image_path = test[1]

            ascii_image_size = test[0]
            ascii_image_path = test[2]

            output = format_image(ascii_image_size, image_path)
            with open(ascii_image_path, "w") as text_file:
                text_file.write(output)


if __name__ == "__main__":
    unittest.main()
