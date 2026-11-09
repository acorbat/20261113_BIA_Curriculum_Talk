# CONTEXT — GloBIAS 2026 talk: "From Diverse Paths to a Common Core"

Working context for building the slide deck. Read this first in any new session.
Last updated: 2026-11-09.

## 0. Working conventions

- **Git: small commits.** One logical change per commit, such as a single slide edit, one figure, or a docs update. Don't bundle unrelated changes. A push can carry several commits, and a clean history comes from many small, focused commits.
- Commits are authored as Agustin Corbat <acorbat@df.uba.ar>. Commits made with Claude end with the Co-Authored-By / Claude-Session trailers.
- The talk folder on Agustín's computer is the source of truth. Edit there (or sync to it), check the result, then commit.

## 1. The talk

| | |
|---|---|
| **Title** | From Diverse Paths to a Common Core: Kickstarting a Bioimage Analysis Curriculum |
| **Venue** | Global BioImage Analysts' Society (GloBIAS) Annual Meeting |
| **Date** | 13 Nov 2026 (from the folder name; please confirm) |
| **Slot** | 20 min talk + 10 min questions |
| **Speaker** | Agustín Corbat, Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires |
| **Local folder** | `Documents\GloBIAS\20261113_BIA_Curriculum_Talk` |
| **Assets so far** | `img/2026016_Agus_archipielago.png/.svg`: a folded map of an archipelago with three islands. **Red** = computing (monitor with a gear), **teal** = biology (cell), **yellow** = physics/optics (prism splitting light). Sailboats in mixed colours travel between them on dashed routes. |

### Abstract (verbatim)
> Bioimage analysts originate from highly diverse academic backgrounds, resulting in varied and non-standardized career paths. To address the challenges this presents for training and professionalization, we will discuss focused on two key objectives. First, we will evaluate whether the community can define a universal "minimum baseline" of core topics that every bioimage analyst should master, specifically examining areas like digital image fundamentals, programming formalisms, and the mechanics of image generation. Second, we aim to kickstart a dedicated Working Group before or during the meeting to explore how to develop this standardized curriculum framework, assuming the community agrees on its necessity. By establishing a clear, community-approved educational foundation, we can better support emerging practitioners, streamline institutional training, and further professionalize the analyst role globally.

### Core message (from the speaker's brief)
1. There is no formal training route for bioimage analysts. People arrive from computer science, physics, biology, and other fields, so each analyst has different blind spots.
2. Some analysts build pipelines where subtle aspects of image formation (PSF, sampling, noise, saturation, bit depth) decide whether a result is valid. These subtleties are easy to miss when they lie outside your own field.
3. Proposal: a **minimum common core** that every analyst covers, plus **electives** (as in a university degree) that complete a profile or specialisation.
4. Build on existing work and point to it. Do not reinvent modules.
5. Call to action: start a **GloBIAS Working Group** to define the curriculum framework.

### Two objectives (from the abstract)
- **O1:** Can the community agree on a universal minimum baseline? Candidate pillars: digital image fundamentals, programming formalisms, mechanics of image generation.
- **O2:** Kickstart a Working Group, before or during the meeting.

## 2. Sources

### 2.1 Tischer et al. 2026, J. Microsc. 304:3–14, doi:10.1111/jmi.70133
"Modular training resources for bioimage analysis." 18 authors: Tischer, Politi, Buchholz, Fazeli, Gritti, Halavatyi, González-Tirado, Hennies, Hodges (The Carpentries), Khan, Kutra, Marcotti, Oezdemir, Schneider, Schorb, Stokkermans, Sun, Vakili. Mainly EMBL and facility staff. Open access, CC-BY. Received Dec 2024, accepted June 2026. PDF supplied by the user (not stored in the folder yet).

**What it is:** the peer-reviewed description of the NEUBIAS training resources (section 2.2).

**Key points for the talk**
- Motivation that matches ours: *"Scientists performing bioimage analysis have a diverse background"* and need theory on **image formation** as well as on processing and analysis algorithms, plus the skills to use software tools (Intro).
- Started in 2019. Between 2021 and 2024 it was used in **at least 25 courses** with **nearly 600 participants** (Table S1).
- About **62 modules** (consolidated as of May 2026) and **9 example courses** with durations and **ECTS** credits (1 ECTS = 30 h).
- Based on **The Carpentries** pedagogy. Each module covers 1–2 concepts in **30–45 min** (to manage cognitive load) and is **software-agnostic**: the concept and activity are separate from the implementation (ImageJ GUI/macro, Python, Galaxy).
- Each module has 9 sections: Motivation, Prerequisites, Learning objectives, Concept map, Figure, Explanations, Activities, Assessment, Follow-up.
- A **module dependency graph** is used to assemble consistent courses.
- Courses lasted 0.5–3 days with 3–18 modules, about 6 modules per day.
- Target audience: master's level and above. The resource is also used in facility project discussions.
- **Evidence of an implicit core:** other resources mostly cover data handling and quantitative extraction, so *"there seems to be an agreement among the community as what is considered an essential bioimage analysis skill."* This supports objective O1.
- Image acquisition and degradation matter for judging whether measurements are reliable. Example from the paper: you can measure object shape, but you need to know the resolution limit.
- **Gaps they name:** ML segmentation/classification/restoration and its validation (e.g. confusion matrix), colocalisation, tracking, data management, EM/MRI/CT, colour spaces for histology, other software (Icy, CellProfiler, KNIME, commercial tools), hosting large data (BioImage Archive).
- **Self-declared limitation:** the modules emphasise practice over depth, and the topics *cover "a minor fraction of the bioimage analysis field."* This is the hook for our talk: modules answer **how to teach X**, while a curriculum answers **what everyone must know, to what level, and in what order, and what is optional**.
- Useful references for a "landscape" slide: Bankhead's *Introduction to Bioimage Analysis* book; Haase's lectures; EPFLx *Image processing and analysis for life scientists*; Coursera/MathWorks; Carpentries *Image processing with Python*; NEUBIAS Academy; ZIDAS; Haase et al. 2024 *A call for FAIR and open-access training materials* (OSF); Sivagurunathan et al. 2024 *Bridging imaging users to imaging analysis — a community survey* (J. Microsc. 296:199–213); Haase et al. 2022 *Hitchhiker's guide through the bio-image analysis software universe*.

### 2.2 NEUBIAS Bioimage Analysis Training Resources — https://neubias.github.io/training-resources/
- Maintained by the NEUBIAS community, CC-BY 4.0, built with Jekyll on GitHub (NEUBIAS/training-resources).
- Example courses (modules / hours / ECTS): Bioimage Inspection 8/6 h/0.4 · Bioimage Analysis 13/9 h/0.6 · Advanced Topics 6/4.5 h/0.3 · Image Data Formats 5/3 h/0.2 · Batch Analysis 6/3.75 h/0.25 · Batch Analysis Essentials 2/2 h/0.13 · Cloud-based BIA 3/1.5 h/0.1 · ImageJ Macro 8/6 h/0.4 · **Image Formation and Imaging Artefacts 12/9 h/0.6**.
- Modules grouped by theme (our grouping):
  - **Digital image fundamentals:** Digital image basics, Data types, Display settings, Spatial calibration, Multichannel, N-dimensional images, Projections, Volume slicing
  - **Image generation:** Image sampling, Optimal sampling, Resolution, Point spread function, Spherical aberrations, Optical sectioning, Thick samples, Sample-preparation artefacts, Illumination/shading artefacts
  - **Data and formats:** Image data formats, Big image data formats, OME-TIFF, OME-Zarr, Remote data access
  - **Processing:** Flat-field, Global/local background, Convolutional, Median, Neighbourhood, Rank, Morphological filters, Stitching, Registration (draft)
  - **Segmentation and measurement:** Thresholding (manual and automatic), Connected components, Watershed, Distance transform, Skeletonisation, Segmentation overview and inspection, DL instance segmentation, Object filtering, Intensity measurements, Shape measurements
  - **Programming formalisms:** Running a script, Recording a script, Variables, Strings and paths, Functions, Loops, Input parameters, Output saving, Commenting, Batch processing, Coding with LLMs, Scripting environment
  - **Infrastructure:** Tool installation, Containers, Cloud batch and interactive analysis
  - **Smart microscopy:** Targeted imaging, Acquisition parameter adjustment, Feedback photomanipulation
  - **Worked workflows:** Nuclei segmentation and shape, Nuclei and cells, Golgi per cell, Noisy object segmentation
- **Takeaway:** all three pillars in the abstract already have good teaching material. What is missing is agreement on which of it is **mandatory**, to what **depth**, and for **whom**.

### 2.3 bia_curriculum (the speaker's prototype) — https://github.com/acorbat/bia_curriculum
- A dependency-aware curriculum stored as YAML, with an interactive explorer (static site, GitHub Pages via Actions: https://acorbat.github.io/bia_curriculum/). CC-BY 4.0. Seeded from the two sources above.
- **Data model:** Subject → Topic → Learning Path. Each topic records learning outcomes, required/recommended prerequisites, estimated time (lecture, practical, self-study), Bloom level, difficulty, **audience prior knowledge (biology / physics / CS: low, medium, high)**, `likely_known_by` / `likely_new_for`, delivery format, assessment, references and maturity. A build script validates IDs and cycles and generates the graph and JSON.
- **Current content:** 9 subjects and 23 topics, all `foundational` and `draft`.
  - Imaging Foundations (7): Intro to BIA, Microscopy modalities, Basic wave optics, Pixel size and sampling, PSF and resolution, Noise models, Imaging artefacts and bias
  - Image Data and Formats (3): File formats and metadata, OME data model, Data management and QC
  - Preprocessing (4): Background/flat-field, Classical denoising, Registration, Deconvolution
  - Segmentation (3): Thresholding, Classical segmentation, Segmentation quality metrics
  - Feature extraction (1) · Statistics and experimental design (2) · Automation and reproducibility (1) · ML in BIA (1) · Domain applications (1: cell biology case study)
- **Three background-aware paths:** BIA for Biologists (19 topics, about 39 h), for Physicists (20 topics, about 41 h), for Computer Scientists (21 topics, about 43 h). Each has "bridge" topics: wave optics, statistics and scripting for biologists; experimental design for physicists; optics, modalities and experimental design for CS.
- **Gaps to fix or acknowledge before the talk:** there is no explicit **digital image fundamentals** topic (arrays, data types and bit depth, display vs data, calibration) and no **programming formalisms** topic beyond the single workflows topic. These are two of the three pillars in the abstract. Consider adding `TOP-digital-image-fundamentals` and `TOP-programming-fundamentals` (mapped to the NEUBIAS modules) so the demo matches the talk. Topic references are still generic (the paper and the site as a whole) rather than specific modules.

## 3. Framing devices
- **Archipelago metaphor (from the existing image):** three islands (CS, biology, physics). Analysts sail from one island and are expected to know all the waters. A curriculum works as a **nautical chart**: a shared core of navigation every sailor learns, plus local charts (electives) for specific waters.
- **Colour code** (taken from the image, reused across the deck): red = computing/programming · yellow = physics/image generation · teal = biology/experimental context · grey/neutral = digital image fundamentals (the sea every route crosses).
- **University-degree analogy:** a common core (*ciclo básico*), then electives (*materias optativas*), then a degree/profile. This also maps onto ECTS, which NEUBIAS already uses.
- **Modules ≠ curriculum:** modules are bricks, and a curriculum is the building code that says what every building must have.

## 4. Decisions log
- **2026-11-02:** Plan v1 drafted (Quarto + reveal.js on GitHub Pages, 19 slides).
- **2026-11-02:** Speaker asked for a demo of "one module, different audiences". Added three slides, **"Resolution, explained to a physicist / a biologist / a research software engineer"** (Abbe/Rayleigh formulas · a 25 nm microtubule that looks ~200 nm wide · diffraction as `gaussian_filter` with σ ≈ 0.21 λ/NA). Prototype animation: `figures/microtubule_psf_animation.py` (25 nm → FWHM ≈ 186 nm at λ 520 nm, NA 1.4). Message: the core fixes the learning outcome, and bridges adapt the way in. Merged slides 3+4, 7+8 and 12+13 to stay within 20 min.

- **2026-11-02:** Speaker details settled: Agustín Corbat, FCEN–UBA. Acknowledge CMA (Centro de Microscopías Avanzadas), GloBIAS and LABI (Latin America Bioimaging). Contact: acorbat@df.uba.ar · LinkedIn https://www.linkedin.com/in/agust%C3%ADn-andr%C3%A9s-corbat-1a7a6b89/ · Bluesky @acorbat.bsky.social (both from acorbat.github.io). No GloBIAS template. Show of hands for the opening. New repo for the deck. Do **not** add topics to bia_curriculum yet.
- **2026-11-02:** RSE animation reworked: a Gaussian PSF kernel slides over the 25 nm microtubule (collected light shown in yellow) while camera pixels fill in on the right, ending with `gaussian_filter`. Apparent width ≈ 184 nm.
- **2026-11-02:** Biologist-slide image: H. Vindin, *Microtubules in Primary Mouse Embryonic Fibroblasts*, CC BY 4.0 (Wikimedia Commons). Fallback: the Fiji sample *Fluorescent Cells* (green = tubulin, public domain). Neither is calibrated. Downloads are blocked by egress, so Agustín saves the files manually.

- **2026-11-02:** LinkedIn corrected to https://www.linkedin.com/in/agustin-andres-corbat/. **Deck built** (Quarto + reveal.js, 1600×900, 24 main slides including 5 section dividers, plus 5 backup slides, speaker notes with target times). Repo to be created by Agustín from this folder; GitHub Pages via Actions (`.github/workflows/publish.yml`). Deck URL assumed `https://acorbat.github.io/20261113_BIA_Curriculum_Talk/` (used in the QR codes).

- **2026-11-09:** Git repo cleaned before the first push. Old animation outputs in `figures/` deleted and purged from history. `refs/` is now git-ignored and purged from history (kept locally). Stray outputs in `figures/` are ignored, while `figures/out/` (used by the slides) and all generating code stay tracked. `CONTEXT.md` and `PLAN.md` are tracked. Added LICENSE (CC BY 4.0) and a License section in the README.

- **2026-11-09:** Logos added. Cover: Departamento de Física + CMA bottom-left, GloBIAS + LABI bottom-right, footer hidden. Thank-you slide (which also holds the contact details): logos of CMA, Departamento de Física, FUNDACEN, GloBIAS and LABI, plus a credit line for the NEUBIAS training resources. Display copies made of the CMA logo (subtitle width fixed) and the LABI logo (white original, cropped and recoloured dark).

- **2026-11-09:** Biologist slide now uses the tubulin channel of the Fiji sample *Fluorescent Cells* (public domain; `img/microtubules/C2-FluorescentCells.png`). Fiji's burned-in info text is cropped off. The zoom box (rows 370–440, cols 340–410) shows filaments fanning out at the cell edge, with contrast set within the zoom. The image has no calibration, so the slide stays qualitative.

- **2026-11-09:** Biologist figure switched to the TIFF (`C2-FluorescentCells.tif`, which is pixel-identical to the PNG it replaces). All panels show raw pixels with no interpolation. Added an intensity profile along a 5-px-wide vertical line in the zoom, which crosses about 7 filaments, each a peak several pixels wide. Profile x-axis is in pixels, since the image has no calibration.

- **2026-11-09:** Zoom moved to Fiji x=350, y=225 (70 px), where parallel filaments sit in the upper right of the big cell. The profile line is at column 20 of the zoom and crosses about 6 filaments. The profile is drawn in teal (biology island) and its marker in white.

- **2026-11-09:** Several edits after a speaker review:
  - LABI now uses its colour logo (a cropped copy, `labi_logo_color_slides.png`).
  - Slide 15 is in English: "core courses + electives".
  - Slide 17 says explicitly that the three pillars come from the physics and computing islands and none covers biology.
  - Slide 22: "M = months after kick-off" is explained, the pilot course is removed from M12, and M0 no longer mentions a sign-up.
  - Slide 23 has no links or QR codes; it just says "find me during the meeting, or contact me later".
  - Slide 24 has two acknowledgement groups (support: FUNDACEN, GloBIAS, Departamento de Física; discussions: CMA, LABI) and a Contact subtitle. Its deck QR code was dropped.

## 5. Open items / to confirm with speaker
- Rehearse and check timing (20 min)
- Create the GitHub repo (`acorbat/globias2026-bia-curriculum-talk`?)
- Whether to cite the Sivagurunathan et al. 2024 survey with numbers (not yet read; must be verified before use)
