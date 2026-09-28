from pathlib import Path

import tomlkit
import zlib
# TOML has no null, so transparent cells (None) are stored as -1.
EMPTY_CELL = -1

# Custom cart extension. The file content is plain TOML.
CART_EXTENSION = ".pyicon"


def _encode_value(value):
    if value is None:
        return EMPTY_CELL
    if isinstance(value, dict):
        return {str(k): _encode_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode_value(v) for v in value]
    return value



def _resolve_cart_path(path) -> Path:
    p = Path(path)
    if p.suffix != CART_EXTENSION:
        p = p.with_suffix(CART_EXTENSION) if p.suffix else Path(str(p) + CART_EXTENSION)
    return p


def save_cart(sprite_data, tilemap=None, sound=None, music=None, path="cart.pyico"):
    cart_path = _resolve_cart_path(path)
    data = {
        'sprites': _encode_value(sprite_data or {}),
        'tilemap': _encode_value(tilemap or {}),
        'sound': _encode_value(sound or {}),
        'music': _encode_value(music or {}),
    }
    with open(cart_path, "w", encoding="utf-8") as toml_file:
        tomlkit.dump(data, toml_file)

    print(f"Data successfully saved to {cart_path}!")
    return cart_path

