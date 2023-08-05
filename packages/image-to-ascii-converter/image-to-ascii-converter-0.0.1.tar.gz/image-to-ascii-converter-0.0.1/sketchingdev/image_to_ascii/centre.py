import math


def calculate_padding_to_centre(total_space, used_space):
    if used_space is 0:
        return 0

    padding = total_space - used_space
    return math.floor(padding / 2) if padding > 0 else 0


def centre_in_container(lines, size):
    def pad_text_left(width, line):
        padding = " " * calculate_padding_to_centre(width, len(line))
        return padding + line

    def pad_lines_top(height, lines):
        result = []
        height_padding = calculate_padding_to_centre(height, len(lines))
        for _ in range(height_padding):
            result.insert(0, "")

        return result + lines

    centred_horizontally = list(map(lambda line: pad_text_left(size[0], line), lines))
    centred_vertically = pad_lines_top(size[1], centred_horizontally)

    return centred_vertically
