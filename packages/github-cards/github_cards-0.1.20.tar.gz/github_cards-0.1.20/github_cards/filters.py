WHITE_HEX = "ffffff"
BLACK_HEX = "000000"


def readable_font_color(background_color: str):
    red, green, blue = _hex_to_rgb(background_color)
    font_color = (
        BLACK_HEX if (red * 0.299 + green * 0.587 + blue * 0.114) > 186 else WHITE_HEX
    )
    return font_color


def _hex_to_rgb(hex_: str):
    if hex_[0] == "#":
        hex_ = hex_[1:]
    return tuple(int(hex_[i : (i + 2)], 16) for i in (0, 2, 4))  # noqa
