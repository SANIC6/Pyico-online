from pathlib import Path

from tools.color_picker import load_palette

COLORS = load_palette(Path(__file__).resolve().parents[1] / "gd-15-32x.png")
