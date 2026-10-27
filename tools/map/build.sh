#!/usr/bin/env bash
# Rebuild the light and dark channel maps in content/channels/.
#
# map.tex is the TikZ overlay from the paper's intro.tex (Figure 1), drawn on
# blank_light.pdf (the paper's fig/blank_map.pdf) or blank_dark.pdf (the same
# map with a transparent ocean, land #4a5057 and outline #9aa1a8).
# Needs pdflatex and pdftocairo (poppler).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/../../content/channels"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cp "$here"/map.tex "$here"/blank_light.pdf "$here"/blank_dark.pdf "$tmp"
cd "$tmp"
pdflatex -interaction=batchmode -jobname=map-light map.tex >/dev/null
pdflatex -interaction=batchmode -jobname=map-dark '\def\darkmode{}\input{map.tex}' >/dev/null
pdftocairo -png -singlefile -scale-to-x 1835 -scale-to-y -1 map-light.pdf "$out/map"
pdftocairo -png -singlefile -transp -scale-to-x 1835 -scale-to-y -1 map-dark.pdf "$out/map-dark"
