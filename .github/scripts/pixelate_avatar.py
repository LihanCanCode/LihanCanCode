"""Fetch a GitHub user's avatar and render it as blocky pixel art."""

import sys

import requests
from PIL import Image

PIXEL_GRID_SIZE = 40
OUTPUT_SIZE = 480


def fetch_avatar(username: str) -> Image.Image:
    url = f"https://github.com/{username}.png?size=460"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open("/tmp/avatar_source.png", "wb") as f:
        f.write(response.content)
    return Image.open("/tmp/avatar_source.png").convert("RGBA")


def pixelate(image: Image.Image) -> Image.Image:
    small = image.resize((PIXEL_GRID_SIZE, PIXEL_GRID_SIZE), resample=Image.BOX)
    return small.resize((OUTPUT_SIZE, OUTPUT_SIZE), resample=Image.NEAREST)


def main() -> None:
    username, output_path = sys.argv[1], sys.argv[2]
    avatar = fetch_avatar(username)
    pixelate(avatar).save(output_path)


if __name__ == "__main__":
    main()
