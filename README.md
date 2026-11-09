# From Diverse Paths to a Common Core: Kickstarting a Bioimage Analysis Curriculum

Slides for the talk at the **GloBIAS Annual Meeting 2026** (20 min + 10 min Q&A).
**Agustín Corbat**, Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires · acorbat@df.uba.ar

Live slides: <https://acorbat.github.io/20261113_BIA_Curriculum_Talk/> (once GitHub Pages is enabled; see below)

## Contents

| Path | What it is |
|---|---|
| `index.qmd` | The deck (Quarto + reveal.js), with speaker notes and target times on every slide |
| `theme/archipelago.scss` | Theme; colours taken from the archipelago map |
| `figures/make_figures.py` | Generates every static figure into `figures/out/` |
| `figures/microtubule_psf_animation.py` | The "PSF as a sliding Gaussian" animation (`figures/out/microtubule_psf.mp4`) |
| `figures/screenshot_explorer.js` | Playwright script used to screenshot the `bia_curriculum` explorer |
| `img/` | Archipelago map; `img/logos/` institutional and community logos; `img/microtubules/` takes the microtubule image (see README there) |
| `PLAN.md`, `CONTEXT.md` | Talk plan, source summaries and decisions log |
| `refs/` | Local copies of cited papers (git-ignored, not redistributed) |

## Build locally

```bash
# figures (only needed if you change them; outputs are committed)
python -m pip install -r figures/requirements.txt
python figures/make_figures.py
python figures/microtubule_psf_animation.py      # needs ffmpeg; ~1–2 min

# slides
quarto preview          # live reload
quarto render           # -> _site/index.html
```

Presenting: press **S** for speaker view (notes + timer), **F** for fullscreen, **Esc** for overview.
Offline backup: open `_site/index.html` from a local copy, or print to PDF from Chrome with `?print-pdf`.

## Publish on GitHub Pages

1. Create the repo from this folder and push to `main`.
2. In the repo go to **Settings › Pages › Source** and choose **GitHub Actions**.
3. Every push to `main` runs `.github/workflows/publish.yml`, which renders the slides and deploys them.

If you name the repo something other than `20261113_BIA_Curriculum_Talk`, update `DECK_URL` in
`figures/make_figures.py`, re-run it (to refresh the QR codes), and update the URL on the "Join us" slide.

## License

Original material in this repository (slides, text, figures, code and the archipelago illustration) is licensed under the
**Creative Commons Attribution 4.0 International (CC BY 4.0)** license; see [`LICENSE`](LICENSE) or
<https://creativecommons.org/licenses/by/4.0/>. Please attribute it to **Agustín Corbat** and link to this repository.
Third-party material keeps its own terms (see Credits); this license does not relicense it.
The institutional and community logos in `img/logos/` belong to their respective organisations and are **not** covered by
CC BY 4.0. `cma_logo_slides.svg` and `labi_logo_slides.svg` are display copies of `cma_logo.svg` and `labi_logo.svg`:
the first fixes the subtitle width for machines without the original fonts, the second is cropped and recoloured dark
for white backgrounds.

## Credits

- Microtubule image: *Fluorescent Cells* (BPAE cells, anti-tubulin channel), ImageJ/Fiji sample image, public domain.
- Module data: NEUBIAS Bioimage Analysis Training Resources (CC BY 4.0); Tischer et al. 2026, *J. Microsc.* 304:3–14.
- Curriculum prototype: <https://github.com/acorbat/bia_curriculum> (CC BY 4.0).
