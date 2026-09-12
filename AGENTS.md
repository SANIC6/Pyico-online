# Pico-online — agent notes

PICO-8-style sprite editor prototype (pygame). No README, no CI, no tests/lint config.

## Commands (uv-managed, Python 3.13)
- `uv sync` — install (`uv.lock`, `.venv/` in workspace)
- `uv run python app.py` — run the real editor (root `app.py:main`)
- `uv run python console/main.py run <cartfile>` — CLI stub (print-only)
- No test/lint/typecheck commands exist — don't invent them.

## Entrypoints — don't confuse
- `app.py` = real app (`Editor.run()` loop). `console/main.py` = throwaway argparse stub. `src/pico_online/__init__.py` = hello stub wired to `pico-online` script (stale, not the app).
- Never `import console.main` — it calls `parse_args()` at module top level.

## Wiring & gotchas
- `tools/constants.py: COLORS` loads root `16-bital.png` at import via `tools/color_picker.py:load_palette()`; returns `dict[int, hex-str]`. Changing the PNG changes palette size; `app.py:draw_pallete` assumes ≤16 entries in a 2×8 grid.
- Display: logical `160×144`, scaled ×4 (`WINDOW_SIZE`, `DISPLAY_SCALE` in `app.py`). Mouse pos is divided by scale then clamped — keep that order.
- Canvas is hard-coded 8×8, `cell_size=8`, `sprite_editor_box=Rect(8,16,64,64)`. Assets resolve relative to `app.py` → `editor/assets/`.
- Deps quirk: both `pygame` and `pygame-ce` in `pyproject.toml`; `logging` is a bogus PyPI shim for stdlib — leave alone unless cleaning up deps.
- `tools/__pycache__/` appears tracked in git; don't commit `*.pyc`. Repo has no `.gitignore`.
