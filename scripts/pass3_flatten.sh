#!/usr/bin/env bash
set -eu
cd "$(git rev-parse --show-toplevel)"

flatten_pkg() {
  pkg="$1"
  [ -d "$pkg" ] || return 0
  find "$pkg" -mindepth 2 -type f | while read -r f; do
    base=$(basename "$f")
    dest="$pkg/$base"
    if [ -e "$dest" ] && [ "$f" != "$dest" ]; then
      dest="$pkg/$(basename "$(dirname "$f")")_$base"
    fi
    git mv "$f" "$dest" 2>/dev/null || mv "$f" "$dest"
  done
  find "$pkg" -mindepth 1 -type d -empty -delete
  find "$pkg" -mindepth 1 -type d ! -name __pycache__ | while read -r d; do
    rmdir "$d" 2>/dev/null || true
  done
  if [ ! -f "$pkg/__init__.py" ]; then
    printf '# %s package\n' "$pkg" > "$pkg/__init__.py"
  fi
}

for p in cognitive adversarial hardening memory engines; do
  flatten_pkg "$p"
done
