# Pico-online — agent notes

PICO-8-style sprite editor prototype (pygame). No README, no CI, no tests/lint config.

## Commands (uv-managed, Python 3.13)
- `uv sync` — install (`uv.lock`, `.venv/` in workspace)
- `uv run python app.py` — run the real editor (root `app.py:main`); needs a display
- `uv run python console/main.py run <cartfile>` — CLI stub (print-only)
- Headless check (no window): `$env:SDL_VIDEODRIVER="dummy"; uv run python -c "import pygame; pygame.init(); from app import Editor; ..."`
- `uv run python -m py_compile app.py` — syntax check. No test/lint/typecheck commands exist — don't invent them.

## Entrypoints — don't confuse
- `app.py` = real app (`Editor.run()` loop). `console/main.py` = throwaway argparse stub. `src/pico_online/__init__.py` = hello stub wired to `pico-online` script (stale, not the app).
- Never `import console.main` — it calls `parse_args()` at module top level.

## Wiring & gotchas
- `tools/constants.py: COLORS` loads root `16-bital.png` at import via `tools/color_picker.py:load_palette()`; returns `dict[int, hex-str]`. Reordering the PNG recolors existing art (canvases store indices, not colors); `app.py:draw_pallete` assumes ≤16 entries in a 2×8 grid.
- Canvas cells store palette indices (`int|None`, `None` = empty/transparent), never hex strings. `Mouse.color_index` is the selected index; `draw_canvas()` resolves `COLORS[c]` guarded by `c in COLORS` (stale indices skip, don't crash); palette highlight compares indices.
- Per-sprite art: `Editor.sprite_data: dict[int, 8×8 grid]`, lazy via `get_or_create_sprite()` (slot 0 seeded at startup; clicking a blank slot creates an empty key). `Mouse.canvas is sprite_data[selected]` — shared reference = write-through, no save step. Blank = all-`None`.
- Sprite bank: `sprites_background=Rect(80,16,72,144)` holds a tight 9×15 grid of 8×8 slots (135). `sprite_rects` is rebuilt every frame by `draw_sprite_slots()`, which must run before `mouse.update()` (hit-testing needs fresh rects). Selected slot gets a 1px white border; slots stay black (no thumbnails).
- Display: logical `160×144`, scaled ×4 (`WINDOW_SIZE`, `DISPLAY_SCALE` in `app.py`). Mouse pos is divided by scale then clamped — keep that order.
- Editor canvas is hard-coded 8×8, `cell_size=8`, `sprite_editor_box=Rect(8,16,64,64)`. Assets resolve relative to `app.py` → `editor/assets/`.
- Deps quirk: both `pygame` and `pygame-ce` in `pyproject.toml`; `logging` is a bogus PyPI shim for stdlib — leave alone unless cleaning up deps.
- `__pycache__/*.pyc` is tracked in git; don't commit `*.pyc`. Repo has no `.gitignore`.
