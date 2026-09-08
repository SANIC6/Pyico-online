"""Load a horizontal-strip palette PNG into an ordered hex dict.

Strip layout: one row of swatches left-to-right. Each swatch may be
1px wide or scaled N px wide — consecutive duplicates are collapsed.

Uses only pygame-ce + numpy (both already in pyproject.toml).
"""

from pathlib import Path

import pygame
import pygame.surfarray




def load_palette(png_path: str | Path, row: int | None = None) -> dict[int, str]:
    """Load palette strip PNG, return {index: '#rrggbb'} left-to-right.

    Args:
        png_path: Path to a PNG strip image.
        row: Which y row to sample. Defaults to middle row (H // 2).

    Raises:
        FileNotFoundError: If the PNG does not exist.
        ValueError: If row is out of range or no pixels found.
    """
    path = Path(png_path)
    if not path.is_file():
        raise FileNotFoundError(f"palette PNG not found: {path}")

    surf = pygame.image.load(str(path))
    # array3d -> (W, H, 3), drops alpha which is what we want.
    arr = pygame.surfarray.array3d(surf)
    width, height, _ = arr.shape
    if width == 0 or height == 0:
        raise ValueError(f"empty image: {path}")

    y = height // 2 if row is None else row
    if not 0 <= y < height:
        raise ValueError(f"row {y} out of range for height {height}")

    palette: dict[int, str] = {}
    last_rgb: tuple[int, int, int] | None = None
    for x in range(width):
        rgb = (int(arr[x, y, 0]), int(arr[x, y, 1]), int(arr[x, y, 2]))
        if rgb == last_rgb:
            continue
        last_rgb = rgb
        palette[len(palette)] = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    if not palette:
        raise ValueError(f"no colors sampled from {path} row {y}")
    return palette


load_in = load_palette
