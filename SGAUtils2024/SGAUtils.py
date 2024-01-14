import hashlib

class SGAUtils():
    bg_colors = [
        "#AEC6CF",  # Pastel Blue
        "#98FF98",  # Mint Green
        "#E6E6FA",  # Lavender
        "#FFD1DC",  # Blush Pink
        "#FFE5B4",  # Peach
        "#FFFACD",  # Baby Yellow
        "#B0E0E6",  # Powder Blue
        "#F08080",  # Light Coral
        "#87CEEB",  # Sky Blue
        "#D8BFD8",  # Thistle
        "#98FB98",  # Pale Green
        "#7FFFD4",  # Aquamarine
        "#FFA07A",  # Light Salmon
        "#C9A0DC",  # Wisteria
        "#FFFACD",  # Lemon Chiffon
        "#AFEEEE"  # Pale Turquoise
    ]
    def __init__(self):
        pass

    def string_to_int_with_hashlib(s):
        # Create a hash object
        hash_object = hashlib.sha256()
        # Update the hash object with the bytes of the string
        hash_object.update(s.encode())
        # Get the hexadecimal digest and convert it to an integer
        return int(hash_object.hexdigest(), 16)

    def rgb_to_hex(r, g, b):
        """ Convert RGB color to hexadecimal format. """
        return f'#{r:02x}{g:02x}{b:02x}'

    def bg_color_from_string(s):
        color_code = SGAUtils.string_to_int_with_hashlib(s)
        bg_color = SGAUtils.bg_colors[color_code % len(SGAUtils.bg_colors)]
        return bg_color

    def read_file_lines_generator(filename):
        with open(filename, 'r', encoding='utf-16') as file:
            for line in file:
                yield line

