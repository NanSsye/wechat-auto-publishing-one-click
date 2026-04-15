#!/usr/bin/env bash
set -euo pipefail

echo '[bootstrap] checking commands'
command -v python3 >/dev/null
command -v node >/dev/null
command -v npm >/dev/null || true
command -v chromium >/dev/null || command -v google-chrome >/dev/null || true

echo '[bootstrap] installing python deps (user site)'
python3 -m pip install --user --quiet pillow playwright cairosvg pyyaml requests || true

echo '[bootstrap] playwright browser install best-effort'
python3 -m playwright install chromium || true

echo '[bootstrap] done'
