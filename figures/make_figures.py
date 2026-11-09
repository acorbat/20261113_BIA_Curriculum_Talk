"""Static figures for the GloBIAS 2026 talk.

    python figures/make_figures.py            # writes everything into figures/out/

Figures
  archipelago_labelled.png   slide 2  - the map with island labels
  archipelago_route.png      slide 18 - the map with a charted common route
  pitfall_uint8.png          slide 4  - 200 + 100 = 44
  pitfall_saturation.png     slide 4  - clipping changes intensity ratios
  pitfall_anisotropy.png     slide 4  - forgetting the z-step
  airy.png                   slide 8  - Airy disk + Rayleigh criterion
  biologist_microtubules.png slide 9  - real microtubule image (or simulated placeholder)
  width_to_scale.png         slide 9  - 25 nm vs ~190 nm, drawn to scale
  qr_deck.svg, qr_curriculum.svg

The microtubule image is read from img/microtubules/ if present (see README there);
otherwise a clearly labelled simulated network is rendered instead.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom
from scipy.special import j1

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "out"
OUT.mkdir(parents=True, exist_ok=True)

# ---- palette (sampled from img/2026016_Agus_archipielago.png) --------------
RED, YELLOW, TEAL = "#D1495B", "#EDAE49", "#00798C"
RED_L, YELLOW_L, TEAL_L = "#D66977", "#EDB969", "#2F909F"
INK, MUTED, LINE = "#1F2328", "#6B7075", "#D0D4D9"

DECK_URL = "https://acorbat.github.io/20261113_BIA_Curriculum_Talk/"
CURRICULUM_URL = "https://github.com/acorbat/bia_curriculum"

# ---- wave-optics parameters shared by slides 8-10 -------------------------
WAVELENGTH_NM, NA = 520.0, 1.4
ABBE_NM = WAVELENGTH_NM / (2 * NA)            # 185.7
RAYLEIGH_NM = 0.61 * WAVELENGTH_NM / NA       # 226.6
FWHM_AIRY_NM = 0.514 * WAVELENGTH_NM / NA     # 190.9
MT_NM = 25.0

_family = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({
    "font.family": _family, "font.size": 16, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.05,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})
MONO = "DejaVu Sans Mono"


def _clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


# ===========================================================================
# Archipelago
# ===========================================================================
# icon centres in the original 5314 x 3797 PNG (measured)
ISLANDS = {
    "computer": dict(xy=(1116, 1209), label="Computer science", color=RED),
    "biology": dict(xy=(3401, 640), label="Biology", color=TEAL),
    "physics": dict(xy=(3095, 2099), label="Physics", color="#C8861B"),
}


def archipelago():
    im = Image.open(ROOT / "img" / "2026016_Agus_archipielago.png").convert("RGBA")
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    s = 0.5
    offsets = {"computer": (0, -330), "biology": (0, -300), "physics": (0, 330)}

    for name, route in (("archipelago_labelled", False), ("archipelago_route", True)):
        fig, ax = plt.subplots(figsize=(13.3, 9.5))
        ax.imshow(im)
        _clean(ax)
        if not route:
            for k, d in ISLANDS.items():
                x, y = d["xy"][0] * s, d["xy"][1] * s
                dx, dy = offsets[k]
                ax.text(x + dx * s, y + dy * s, d["label"], ha="center", va="center", fontsize=24,
                        fontweight="bold", color=d["color"],
                        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=d["color"], lw=2, alpha=0.92))
        else:
            # a charted route: every island -> common core (compass-rose style hub) -> electives beyond
            hub = np.array([2600, 1310]) * s
            for k, d in ISLANDS.items():
                p = np.array(d["xy"]) * s
                ax.annotate("", xy=hub, xytext=p,
                            arrowprops=dict(arrowstyle="-|>", lw=6, color=d["color"], ls=(0, (3, 1.5)),
                                            shrinkA=30, shrinkB=46, mutation_scale=34,
                                            connectionstyle="arc3,rad=0.12"))
            ax.scatter(*hub, s=7500, color="white", ec=INK, lw=3.5, zorder=5)
            ax.text(*hub, "common\ncore", ha="center", va="center", fontsize=17, fontweight="bold",
                    color=INK, zorder=6, linespacing=1.0)
        fig.savefig(OUT / f"{name}.png", dpi=110)
        plt.close(fig)


# ===========================================================================
# Pitfalls (slide 4)
# ===========================================================================
def pitfall_uint8():
    y, x = np.mgrid[-1:1:200j, -1:1:200j]
    blob = (200 * np.exp(-(x**2 + y**2) / 0.25)).astype(np.uint8)
    brighter = blob + np.uint8(100)          # wraps around in uint8 (numpy keeps the dtype)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 4.1))
    for ax, img, t in zip(axs, [blob, brighter], ["img", "img + 100"]):
        ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        _clean(ax)
        ax.set_title(t, family=MONO, fontsize=19, color=INK)
    axs[1].annotate("200 + 100 = 44", xy=(100, 100), xytext=(100, 186), ha="center", fontsize=17,
                    family=MONO, color=RED, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    fig.suptitle("uint8 overflow: the brightest pixels turn dark", fontsize=18, color=INK, y=1.02)
    fig.savefig(OUT / "pitfall_uint8.png")
    plt.close(fig)


def pitfall_saturation():
    x = np.linspace(0, 10, 1000)
    true = 120 * np.exp(-(x - 3) ** 2 / 0.6) + 360 * np.exp(-(x - 7) ** 2 / 0.6) + 10
    rec = np.minimum(true, 255)
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(x, true, color=MUTED, lw=2, ls="--", label="true signal")
    ax.plot(x, rec, color=YELLOW, lw=3.5, label="recorded (8-bit)")
    ax.axhline(255, color=RED, lw=1.2, ls=":")
    ax.text(4.6, 262, "255 = detector max", color=RED, fontsize=13, ha="center", va="bottom")
    ax.set_xlabel("position"); ax.set_ylabel("intensity")
    ax.set_xticks([]); ax.set_ylim(0, 400)
    ax.legend(frameon=False, loc="upper left", fontsize=13)
    ax.text(5.9, 160, "true ratio  3.0\nmeasured    2.1", ha="right", va="bottom", fontsize=14, color=INK, family=MONO)
    ax.set_title("saturation: clipped cells under-report expression", fontsize=18, color=INK)
    fig.savefig(OUT / "pitfall_saturation.png")
    plt.close(fig)


def pitfall_anisotropy():
    # 6 um sphere, xy pixel 0.1 um, z-step 0.5 um
    xy, dz, d = 0.1, 0.5, 6.0
    xs = np.arange(-4, 4, xy) + xy / 2
    zs = np.arange(-4, 4, dz) + dz / 2
    X, Z = np.meshgrid(xs, zs)
    xz = (X**2 + Z**2 <= (d / 2) ** 2).astype(float)
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 4.1), layout="constrained")
    axs[0].imshow(xz, cmap="gray", aspect=1.0, interpolation="nearest")      # voxels treated as cubes
    axs[0].set_title("voxels assumed cubic", fontsize=16, color=RED)
    axs[1].imshow(xz, cmap="gray", aspect=dz / xy, interpolation="nearest")  # calibrated
    axs[1].set_title("z-step = 5 × pixel", fontsize=16, color=TEAL)
    for ax in axs:
        _clean(ax)
    fig.supxlabel("xz view of a 6 µm sphere: volume off by 5×", fontsize=16, color=INK)
    fig.suptitle("anisotropic voxels: shape & volume distorted", fontsize=18, color=INK)
    fig.savefig(OUT / "pitfall_anisotropy.png")
    plt.close(fig)


# ===========================================================================
# Physicist slide (8): Airy pattern + Rayleigh criterion
# ===========================================================================
def airy_intensity(r_nm):
    v = 2 * np.pi * NA * np.asarray(r_nm, float) / WAVELENGTH_NM
    out = np.ones_like(v)
    nz = v != 0
    out[nz] = (2 * j1(v[nz]) / v[nz]) ** 2
    return out


def airy():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw=dict(width_ratios=[1, 1.5]))
    g = np.linspace(-700, 700, 501)
    X, Y = np.meshgrid(g, g)
    I = airy_intensity(np.hypot(X, Y))
    cmap = LinearSegmentedColormap.from_list("y", ["black", "#7A4E0A", YELLOW, "white"])
    axs[0].imshow(I ** 0.35, cmap=cmap, extent=[-700, 700, -700, 700])   # gamma to show the rings
    axs[0].add_patch(plt.Circle((0, 0), RAYLEIGH_NM, fill=False, ec="white", ls="--", lw=1.5))
    axs[0].text(0, -RAYLEIGH_NM - 70, f"first zero: {RAYLEIGH_NM:.0f} nm", color="white", ha="center",
                va="top", fontsize=13)
    axs[0].plot([300, 600], [-620, -620], color="white", lw=4)
    axs[0].text(450, -580, "300 nm", color="white", ha="center", fontsize=12)
    _clean(axs[0])
    axs[0].set_title("Airy disk (λ = 520 nm, NA 1.4)", fontsize=16, color=INK)

    x = np.linspace(-700, 700, 2001)
    a = airy_intensity(np.abs(x + RAYLEIGH_NM / 2))
    b = airy_intensity(np.abs(x - RAYLEIGH_NM / 2))
    ax = axs[1]
    ax.fill_between(x, a, color=YELLOW_L, alpha=0.35, lw=0)
    ax.fill_between(x, b, color=YELLOW_L, alpha=0.35, lw=0)
    ax.plot(x, a + b, color=INK, lw=2.5, label="two point sources")
    dip = (a + b)[len(x) // 2] / (a + b).max()
    ax.annotate("", xy=(-RAYLEIGH_NM / 2, 1.08), xytext=(RAYLEIGH_NM / 2, 1.08),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
    ax.text(0, 1.13, f"Rayleigh: {RAYLEIGH_NM:.0f} nm", color=RED, ha="center", fontsize=15)
    ax.text(0, (a + b)[len(x) // 2] - 0.12, f"centre ≈ {dip * 100:.0f} % of peak", ha="center", fontsize=13, color=MUTED)
    ax.set_xlim(-600, 600); ax.set_ylim(0, 1.25)
    ax.set_xlabel("position (nm)"); ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title("just resolved", fontsize=16, color=INK)
    fig.tight_layout()
    fig.savefig(OUT / "airy.png")
    plt.close(fig)


# ===========================================================================
# Biologist slide (9)
# ===========================================================================
# Per-image settings for the biologist slide, keyed by a substring of the file name.
#   crop  : (row0, row1, col0, col1) region kept from the image (None = whole image)
#   zoom  : (row, col, size) of the zoom box, in pixels of the cropped image
#   profile: vertical line inside the zoom (col, (row0, row1), width in px averaged across)
#   credit: line printed under the figure
# All panels show raw pixels (no interpolation); the profile uses the raw 8-bit values.
MICROTUBULE_SOURCES = {
    "FluorescentCells": dict(           # Fiji › File › Open Samples › Fluorescent Cells, tubulin channel
        crop=(0, 465, 0, 512),           # drops Fiji's burned-in "Press 'I' (Image>Show Info)…" overlay
        zoom=(225, 350, 70),                           # Fiji x=350, y=225: parallel filaments, upper right of the big cell
        profile=dict(col=20, rows=(4, 64), width=5),   # vertical line in zoom coordinates, crossing ~6 filaments
        credit="Image: Fluorescent Cells, ImageJ/Fiji sample (public domain)",
    ),
    "Vindin": dict(
        crop=None, zoom=None, profile=None,
        credit="Image: H. Vindin, Microtubules in primary mouse embryonic fibroblasts, CC BY 4.0, Wikimedia Commons",
    ),
}
CYAN = LinearSegmentedColormap.from_list("cyan", ["black", "#0B4F5A", "#2FB5C8", "#DFFBFF"])


def _simulated_network(n=900, px_nm=65.0, seed=3):
    """Simulated microtubule network: 25 nm filaments blurred by a Gaussian PSF."""
    rng = np.random.default_rng(seed)
    fine = 5                                   # simulate on a 13 nm grid, then sample
    N = n * fine
    obj = np.zeros((N, N), np.float32)
    for _ in range(140):
        p = rng.uniform(0.2, 0.8, 2) * N
        ang = rng.uniform(0, 2 * np.pi)
        for _ in range(2500):
            ang += rng.normal(0, 0.03)
            p = p + 3 * np.array([np.cos(ang), np.sin(ang)])
            i, j = int(p[0]), int(p[1])
            if not (0 <= i < N and 0 <= j < N):
                break
            obj[i, j] = 1
    sigma_px = 0.21 * WAVELENGTH_NM / NA / (px_nm / fine)
    img = gaussian_filter(obj, sigma_px)[::fine, ::fine]
    img = rng.poisson(img / img.max() * 120 + 3).astype(float)
    return img


def biologist():
    folder = ROOT / "img" / "microtubules"
    src = sorted(p for p in folder.glob("*") if p.suffix.lower() in (".png", ".tif", ".tiff", ".jpg"))
    simulated = not src
    cfg = dict(crop=None, zoom=None, profile=None, credit=None)
    if simulated:
        raw = _simulated_network()
    else:
        cfg.update(next((c for k, c in MICROTUBULE_SOURCES.items() if k.lower() in src[0].name.lower()), {}))
        im = Image.open(src[0])
        raw = np.asarray(im.convert("RGB")).max(axis=2).astype(float) if im.mode in ("P", "RGB", "RGBA") \
            else np.asarray(im).astype(float)  # single-colour LUT: brightest channel = intensity
        if cfg["crop"]:
            r0, r1, c0, c1 = cfg["crop"]
            raw = raw[r0:r1, c0:c1]
    lo, hi = np.percentile(raw, 1), np.percentile(raw, 99.7)
    disp = np.clip((raw - lo) / (hi - lo), 0, 1)              # display only; profile uses raw values

    h, w = raw.shape
    cy, cx, bs = cfg["zoom"] or (int(h * 0.30), int(w * 0.42), h // 6)
    prof = cfg["profile"] or dict(col=bs // 2, rows=(2, bs - 2), width=3)

    from matplotlib.gridspec import GridSpec
    H = 6.0
    right_w = H * 0.62                                          # zoom is square, 62 % of the height
    fig = plt.figure(figsize=(H * w / h + right_w + 0.5, H))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[H * w / h, right_w], height_ratios=[0.62, 0.38],
                  left=0.005, right=0.99, top=0.93, bottom=0.10, wspace=0.07, hspace=0.36)
    ax_o = fig.add_subplot(gs[:, 0]); ax_z = fig.add_subplot(gs[0, 1]); ax_p = fig.add_subplot(gs[1, 1])

    ax_o.imshow(disp, cmap=CYAN, interpolation="nearest")
    ax_o.add_patch(plt.Rectangle((cx - 0.5, cy - 0.5), bs, bs, fill=False, ec="white", lw=2))
    z_raw = raw[cy:cy + bs, cx:cx + bs]
    zlo, zhi = np.percentile(z_raw, 1), np.percentile(z_raw, 99.5)  # contrast set within the zoom
    ax_z.imshow(np.clip((z_raw - zlo) / (zhi - zlo), 0, 1), cmap=CYAN, interpolation="nearest")
    c, (p0, p1), pw = prof["col"], prof["rows"], prof["width"]
    ax_z.add_patch(plt.Rectangle((c - pw / 2, p0 - 0.5), pw, p1 - p0, fill=False, ec="white", lw=2))
    for ax in (ax_o, ax_z):
        _clean(ax)
    ax_z.set_title("zoom (raw pixels)", fontsize=17, color=INK)

    values = z_raw[p0:p1, c - pw // 2:c + pw // 2 + 1].mean(axis=1)
    pos = np.arange(p0, p1) - p0
    ax_p.step(pos, values, where="mid", color=TEAL, lw=2.2)          # biology island colour
    ax_p.fill_between(pos, values, step="mid", color=TEAL_L, alpha=0.25, lw=0)
    ax_p.set_xlim(pos[0] - 0.5, pos[-1] + 0.5)
    ax_p.set_xlabel("pixels along the line", fontsize=16)
    ax_p.set_ylabel("intensity", fontsize=16)
    ax_p.tick_params(labelsize=14)
    ax_p.set_title("each filament → a wide peak", fontsize=17, color=INK)

    if simulated:
        ax_o.text(0.5, 0.5, "SIMULATED\nplaceholder", transform=ax_o.transAxes, ha="center", va="center",
                  fontsize=34, color="white", alpha=0.35, fontweight="bold", rotation=20)
        credit = "Simulated network (placeholder): replace with img/microtubules/<image>.tif"
    else:
        credit = cfg["credit"] or f"Image: {src[0].stem}"
    fig.text(0.005, 0.0, credit, fontsize=12, color=MUTED)
    fig.savefig(OUT / "biologist_microtubules.png")
    plt.close(fig)


def width_to_scale():
    """25 nm microtubule vs its ~190 nm image, drawn at the same scale."""
    fig, ax = plt.subplots(figsize=(7.5, 2.6))
    x = np.linspace(-300, 300, 1201)
    obj = (np.abs(x) <= MT_NM / 2).astype(float)
    img = gaussian_filter(obj, (0.21 * WAVELENGTH_NM / NA) / (x[1] - x[0]))
    img /= img.max()
    ax.fill_between(x, img, color=TEAL_L, alpha=0.35, lw=0)
    ax.plot(x, img, color=TEAL, lw=2.5)
    ax.fill_between(x, obj, step="mid", color=INK, lw=0)
    ax.annotate("", xy=(-FWHM_AIRY_NM / 2, 0.5), xytext=(FWHM_AIRY_NM / 2, 0.5),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2))
    ax.text(FWHM_AIRY_NM / 2 + 15, 0.5, "image ≈ 190 nm", color=TEAL, va="center", fontsize=15)
    ax.annotate("microtubule 25 nm", xy=(-MT_NM / 2, 0.92), xytext=(-290, 0.92), color=INK, va="center",
                fontsize=15, arrowprops=dict(arrowstyle="->", color=INK, lw=1.5))
    ax.set_xlim(-300, 300); ax.set_ylim(0, 1.1)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("nm (same scale)")
    fig.savefig(OUT / "width_to_scale.png")
    plt.close(fig)


# ===========================================================================
# bia_curriculum explorer screenshot (made by figures/screenshot_explorer.js)
# ===========================================================================
def crop_explorer():
    src = OUT / "explorer_psf.png"
    if not src.exists():
        return
    im = Image.open(src)
    W, H = im.size                       # 2400 x 1350 (1600 x 900 @1.5x)
    im.crop((int(W * 0.195), int(H * 0.12), W, H)).save(OUT / "explorer_psf_crop.png")


# ===========================================================================
# QR codes
# ===========================================================================
def qr_codes():
    import segno
    segno.make(DECK_URL, error="m").save(OUT / "qr_deck.svg", scale=10, border=1, dark=INK)
    segno.make(CURRICULUM_URL, error="m").save(OUT / "qr_curriculum.svg", scale=10, border=1, dark=TEAL)


if __name__ == "__main__":
    archipelago()
    pitfall_uint8(); pitfall_saturation(); pitfall_anisotropy()
    airy()
    biologist(); width_to_scale()
    qr_codes()
    crop_explorer()
    print(f"Abbe {ABBE_NM:.1f} nm · Rayleigh {RAYLEIGH_NM:.1f} nm · Airy FWHM {FWHM_AIRY_NM:.1f} nm")
    print("written:", sorted(p.name for p in OUT.iterdir()))
