from pathlib import Path

# pyrefly: ignore [missing-import]
from pico_online.tools.color_picker import load_palette

COLORS = load_palette(Path(__file__).resolve().parents[1] / "tools/16-bital.png")
