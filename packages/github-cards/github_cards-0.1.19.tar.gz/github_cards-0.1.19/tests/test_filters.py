import pytest

from github_cards.filters import BLACK_HEX, WHITE_HEX, readable_font_color


@pytest.mark.parametrize(
    "background_color, expected",
    [
        (BLACK_HEX, WHITE_HEX),
        (WHITE_HEX, BLACK_HEX),
        ("3993f9", WHITE_HEX),
        ("efe85f", BLACK_HEX),
        ("b52edb", WHITE_HEX),
        ("3E4B9E", WHITE_HEX),
        ("ee0701", WHITE_HEX),
        ("EDDDC2", BLACK_HEX),
    ],
)
def test_readable_font_color_filter(background_color, expected):
    assert readable_font_color(background_color) == expected
