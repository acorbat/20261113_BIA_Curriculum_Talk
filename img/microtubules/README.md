# Microtubule image for slide 9 ("Resolution, explained to a biologist")

Put **one** image here and re-run `python figures/make_figures.py`.
If this folder has no image, a clearly labelled *simulated* network is used instead.

**Preferred:** *Microtubules in Primary Mouse Embryonic Fibroblasts* by Howard Vindin, CC BY 4.0
- Page: https://commons.wikimedia.org/wiki/File:Microtubules_in_Primary_Mouse_Embryonic_Fibroblasts.png
- File: https://upload.wikimedia.org/wikipedia/commons/a/a3/Microtubules_in_Primary_Mouse_Embryonic_Fibroblasts.png
- Save as `Vindin_pMEF_microtubules_CC-BY-4.0.png` (the name containing "Vindin" puts the credit line on the slide automatically).

**Fallback:** Fiji › File › Open Samples › *Fluorescent Cells* (BPAE cells; green = tubulin; public domain).
Save as `FluorescentCells.tif` (the script uses the green channel).

Neither image states its pixel size, so the slide stays qualitative.
Adjust `ZOOM_CENTRE` in `figures/make_figures.py` if the zoom box lands on an empty area.
