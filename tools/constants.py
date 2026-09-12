from pathlib import Path

# pyrefly: ignore [missing-import]
from tools.color_picker import load_palette

COLORS = load_palette(Path(__file__).resolve().parents[1] / "16-bital.png")
