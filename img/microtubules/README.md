# Microtubule image for slide 9 ("Resolution, explained to a biologist")

`C2-FluorescentCells.tif` is the tubulin channel (C2) of the Fiji sample *Fluorescent Cells*
(Fiji › File › Open Samples › Fluorescent Cells; BPAE cells, anti-tubulin; public domain), saved as an 8-bit TIFF with a cyan LUT.

`figures/make_figures.py` reads the first image in this folder and uses the matching entry in `MICROTUBULE_SOURCES`:
- `crop` drops the "Press 'I' (Image>Show Info)…" text that Fiji burns into the bottom-right corner;
- `zoom` sets the zoom box (row, col, size in pixels);
- `profile` sets the intensity-profile line inside the zoom (column, row range, width in pixels averaged across).

All panels show raw pixels (no interpolation), and the profile plots the raw 8-bit values.
- `credit` sets the line printed under the figure.

The image has no pixel-size calibration, so the slide stays qualitative.
If this folder has no image, a clearly labelled *simulated* network is used instead.

Alternative: *Microtubules in Primary Mouse Embryonic Fibroblasts* by Howard Vindin, CC BY 4.0
(https://commons.wikimedia.org/wiki/File:Microtubules_in_Primary_Mouse_Embryonic_Fibroblasts.png); a file name
containing "Vindin" selects its credit line.
