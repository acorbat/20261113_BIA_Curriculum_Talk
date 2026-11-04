"""Diffraction as a sliding Gaussian: how a 25 nm microtubule becomes a ~190 nm line.

Animation for the 'resolution, explained to a research software engineer' slide.

Left panel : the object (a 25 nm wide microtubule on a 5 nm grid) with the PSF,
             a Gaussian kernel, sliding over it pixel by pixel.
Right panel: the camera image. Each pixel takes the value
             image[i, j] = sum(object * psf_centred_on_pixel(i, j))
             at the moment the kernel visits it. The scan starts slowly and then
             speeds up. The finished image is exactly gaussian_filter(object, sigma)
             sampled at the pixel centres.

PSF approximated by a Gaussian with sigma ~= 0.21 * lambda / NA
(widefield approximation; Zhang, Zerubia & Olivo-Marin 2007, Appl. Opt. 46:1819).

Usage:  python figures/microtubule_psf_animation.py [--out figures/out/microtubule_psf] [--fps 30]
Writes <out>.mp4 (reveal.js <video>), <out>.gif (fallback) and <out>_final.png (PDF export).
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation, PillowWriter
from matplotlib.colors import to_rgb
from matplotlib.patches import Circle, ConnectionPatch, Rectangle
from scipy.ndimage import distance_transform_edt, gaussian_filter

# ---- physical parameters -------------------------------------------------
WAVELENGTH_NM = 520.0   # GFP-like emission
NA = 1.4                # oil objective
MT_DIAMETER_NM = 25.0   # microtubule outer diameter
GRID_NM = 5.0           # fine "object" grid
CAMERA_PX_NM = 65.0     # e.g. 6.5 um camera pixel / 100x objective
N_CAM = 24              # camera pixels per side (1.56 µm field)
SIGMA_NM = 0.21 * WAVELENGTH_NM / NA                    # ~78 nm
FWHM_PSF_NM = 2 * np.sqrt(2 * np.log(2)) * SIGMA_NM     # ~184 nm

STEP = int(CAMERA_PX_NM / GRID_NM)       # 13 fine px per camera px
N_FINE = N_CAM * STEP                    # 312
FIELD_NM = N_FINE * GRID_NM              # 1560 nm
CENTRES = STEP // 2 + STEP * np.arange(N_CAM)   # camera pixel centres on the fine grid

# ---- deck palette (from the archipelago map) -----------------------------
TEAL, RED, YELLOW, INK, MUTED = "#00798C", "#D1495B", "#EDAE49", "#222222", "#6B7075"
KERNEL = "#FF5C70"   # brighter red so the PSF reads on black


def centreline(n=4000):
    """Gently curved filament crossing the field top -> bottom (coordinates in nm)."""
    t = np.linspace(-0.1, 1.1, n)
    y = t * FIELD_NM
    x = FIELD_NM * (0.30 + 0.38 * t + 0.07 * np.sin(2 * np.pi * t))
    return x, y


def make_object():
    x, y = centreline()
    raster = np.ones((N_FINE, N_FINE), bool)
    xi, yi = np.round(x / GRID_NM - 0.5).astype(int), np.round(y / GRID_NM - 0.5).astype(int)
    ok = (xi >= 0) & (xi < N_FINE) & (yi >= 0) & (yi < N_FINE)
    raster[yi[ok], xi[ok]] = False
    dist_nm = distance_transform_edt(raster) * GRID_NM
    return (dist_nm <= MT_DIAMETER_NM / 2).astype(float)


def schedule(fps):
    """How many camera pixels are revealed at each animation frame."""
    n_total = N_CAM * N_CAM
    counts, done = [], 0
    for _ in range(N_CAM):                     # row 0: slow, one pixel every 4 frames
        done += 1
        counts += [done] * 4
    for _ in range(N_CAM):                     # row 1: one pixel per frame
        done += 1
        counts.append(done)
    rate = 1.0
    while done < n_total:                      # then accelerate gently, capped
        done = min(n_total, done + int(rate))
        counts.append(done)
        rate = min(rate * 1.06, 8.0)
    return counts


def fwhm_across(img_fine):
    """Apparent width of the blurred filament, measured perpendicular to it."""
    x, y = centreline()
    i = len(x) // 2
    tx, ty = x[i + 1] - x[i - 1], y[i + 1] - y[i - 1]
    nx, ny = -ty / np.hypot(tx, ty), tx / np.hypot(tx, ty)
    s = np.linspace(-500, 500, 2001)
    px, py = (x[i] + s * nx) / GRID_NM - 0.5, (y[i] + s * ny) / GRID_NM - 0.5
    from scipy.ndimage import map_coordinates
    p = map_coordinates(img_fine, [py, px], order=1)
    above = s[p >= p.max() / 2]
    return above[-1] - above[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "out" / "microtubule_psf"))
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()
    fps = args.fps

    obj = make_object()
    blurred = gaussian_filter(obj, SIGMA_NM / GRID_NM, mode="constant", truncate=4.0)
    camera = blurred[np.ix_(CENTRES, CENTRES)]          # == sum(object * kernel) per pixel
    vmax = camera.max()
    width_nm = fwhm_across(blurred)

    # Gaussian kernel sprite (for drawing only)
    r = 3.5 * SIGMA_NM
    g = np.linspace(-r, r, 141)
    gx, gy = np.meshgrid(g, g)
    kern = np.exp(-(gx**2 + gy**2) / (2 * SIGMA_NM**2))
    sprite = np.zeros(kern.shape + (4,))
    sprite[..., :3] = to_rgb(KERNEL)
    sprite[..., 3] = 0.9 * kern
    # same kernel on the fine grid, for the "collected light" highlight
    R = int(np.ceil(r / GRID_NM))
    kf = np.arange(-R, R + 1) * GRID_NM
    kern_fine = np.exp(-(kf[:, None] ** 2 + kf[None, :] ** 2) / (2 * SIGMA_NM**2))

    counts = schedule(fps)
    intro = int(1.5 * fps)        # object alone
    kernel_in = int(1.0 * fps)    # kernel shown on first pixel, nothing computed yet
    outro = int(4.0 * fps)        # finished image + punchline
    n_frames = intro + kernel_in + len(counts) + outro

    # ---- figure layout ----------------------------------------------------
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15})
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor="white")
    ax_l = fig.add_axes([0.05, 0.14, 0.38, 0.675])
    ax_r = fig.add_axes([0.57, 0.14, 0.38, 0.675])
    ax_top = fig.add_axes([0, 0.89, 1, 0.11]); ax_top.axis("off")
    ax_bot = fig.add_axes([0, 0.0, 1, 0.11]); ax_bot.axis("off")

    ext = [0, FIELD_NM, FIELD_NM, 0]
    ax_l.imshow(obj, cmap="gray", extent=ext, vmin=0, vmax=1, interpolation="nearest")
    k_img = ax_l.imshow(sprite, extent=[0, 1, 1, 0], interpolation="bilinear", visible=False, zorder=3)
    glow = np.zeros((N_FINE, N_FINE, 4)); glow[..., :3] = to_rgb(YELLOW)
    g_img = ax_l.imshow(glow, extent=ext, interpolation="nearest", zorder=4, visible=False)
    k_ring = Circle((0, 0), FWHM_PSF_NM / 2, fill=False, ec=KERNEL, lw=1.8, ls="--", visible=False, zorder=4)
    k_px = Rectangle((0, 0), CAMERA_PX_NM, CAMERA_PX_NM, fill=False, ec=YELLOW, lw=2, visible=False, zorder=5)
    ax_l.add_patch(k_ring); ax_l.add_patch(k_px)
    ax_l.set_title("object: a 25 nm microtubule", color=TEAL, fontsize=16, pad=10)

    cmap = plt.get_cmap("gray").copy()
    cmap.set_bad("#EEEEEE")
    r_img = ax_r.imshow(np.ma.masked_all((N_CAM, N_CAM)), cmap=cmap, extent=ext, vmin=0, vmax=vmax,
                        interpolation="nearest")
    for k in range(N_CAM + 1):                 # faint camera pixel grid
        ax_r.axhline(k * CAMERA_PX_NM, color="white", lw=0.4, alpha=0.6, zorder=2)
        ax_r.axvline(k * CAMERA_PX_NM, color="white", lw=0.4, alpha=0.6, zorder=2)
    r_px = Rectangle((0, 0), CAMERA_PX_NM, CAMERA_PX_NM, fill=False, ec=RED, lw=2.5, visible=False, zorder=5)
    ax_r.add_patch(r_px)
    cx, cy = centreline()
    (truth_line,) = ax_r.plot(cx, cy, color=TEAL, lw=1.2, alpha=0.0, zorder=4)
    ax_r.set_title("camera image (65 nm pixels)", color=INK, fontsize=16, pad=10)

    for ax in (ax_l, ax_r):
        ax.set_xlim(0, FIELD_NM); ax.set_ylim(FIELD_NM, 0)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    # 500 nm scale bar on the object panel
    ax_l.plot([FIELD_NM - 580, FIELD_NM - 80], [FIELD_NM - 80] * 2, color="white", lw=4, zorder=6)
    ax_l.text(FIELD_NM - 330, FIELD_NM - 125, "500 nm", color="white", ha="center", fontsize=12, zorder=6)

    code = ax_top.text(0.5, 0.42, "", family="DejaVu Sans Mono", fontsize=19, color=RED, ha="center")
    cap = ax_bot.text(0.05, 0.5, "", fontsize=16, color=INK, va="center")
    readout = ax_bot.text(0.95, 0.5, "", fontsize=14, color=MUTED, va="center", ha="right",
                          family="DejaVu Sans Mono")
    holder = {"con": None}

    def place_kernel(i, j):
        x0, y0 = CENTRES[j] * GRID_NM + GRID_NM / 2, CENTRES[i] * GRID_NM + GRID_NM / 2
        k_img.set_extent([x0 - r, x0 + r, y0 + r, y0 - r])
        k_ring.center = (x0, y0)
        k_px.set_xy((x0 - CAMERA_PX_NM / 2, y0 - CAMERA_PX_NM / 2))
        # highlight the object light collected by the kernel (object * kernel)
        ci, cj = CENTRES[i], CENTRES[j]
        r0, r1 = max(ci - R, 0), min(ci + R + 1, N_FINE)
        c0, c1 = max(cj - R, 0), min(cj + R + 1, N_FINE)
        glow[..., 3] = 0
        glow[r0:r1, c0:c1, 3] = obj[r0:r1, c0:c1] * kern_fine[r0 - ci + R:r1 - ci + R, c0 - cj + R:c1 - cj + R]
        g_img.set_data(glow)
        r_px.set_xy((j * CAMERA_PX_NM, i * CAMERA_PX_NM))
        if holder["con"] is not None:
            holder["con"].remove()
        holder["con"] = ConnectionPatch(xyA=(x0 + CAMERA_PX_NM / 2, y0), coordsA="data", axesA=ax_l,
                                        xyB=(j * CAMERA_PX_NM, (i + 0.5) * CAMERA_PX_NM), coordsB="data",
                                        axesB=ax_r, color=RED, lw=1.5, alpha=0.8,
                                        arrowstyle="-|>", mutation_scale=16, zorder=10)
        fig.add_artist(holder["con"])

    def set_kernel_visible(v):
        for a in (k_img, g_img, k_ring, k_px, r_px):
            a.set_visible(v)
        if holder["con"] is not None:
            holder["con"].set_visible(v)

    def show_pixels(n):
        flat = np.full(N_CAM * N_CAM, np.nan)
        flat[:n] = camera.ravel()[:n]
        r_img.set_data(np.ma.masked_invalid(flat.reshape(N_CAM, N_CAM)))

    def update(f):
        if f < intro:
            set_kernel_visible(False); show_pixels(0)
            code.set_text("")
            cap.set_text("Reality: a microtubule is ~25 nm wide.")
            readout.set_text("")
        elif f < intro + kernel_in:
            place_kernel(0, 0); set_kernel_visible(True); show_pixels(0)
            code.set_text("image[i, j] = (object * psf_at(i, j)).sum()")
            cap.set_text(f"Each camera pixel sees the object through the PSF: a Gaussian, σ ≈ {SIGMA_NM:.0f} nm.")
            readout.set_text(f"λ = {WAVELENGTH_NM:.0f} nm · NA = {NA}")
        elif f < intro + kernel_in + len(counts):
            n = counts[f - intro - kernel_in]
            i, j = divmod(n - 1, N_CAM)
            place_kernel(i, j); set_kernel_visible(True); show_pixels(n)
            code.set_text("image[i, j] = (object * psf_at(i, j)).sum()")
            if n <= N_CAM:
                cap.set_text("Slide the kernel, sum the light it collects (yellow), write one pixel…")
            elif n <= 2 * N_CAM:
                cap.set_text("…next pixel, next pixel…")
            else:
                cap.set_text("…for every pixel: that is a convolution.")
            readout.set_text(f"pixel ({i:2d},{j:2d}) = {camera[i, j] / vmax:.2f}")
        else:
            set_kernel_visible(False); show_pixels(N_CAM * N_CAM)
            t = min(1.0, (f - intro - kernel_in - len(counts)) / (0.6 * fps))
            truth_line.set_alpha(0.9 * t)
            code.set_text("image = gaussian_filter(object, sigma=σ)")
            cap.set_text(f"A 25 nm filament now looks ~{width_nm:.0f} nm wide (≈{width_nm / MT_DIAMETER_NM:.0f}×). "
                         "Teal line: the real one.")
            readout.set_text("")
        return ()

    anim = FuncAnimation(fig, update, frames=n_frames, blit=False)
    anim.save(f"{args.out}.mp4", writer=FFMpegWriter(fps=fps, bitrate=2400, extra_args=["-pix_fmt", "yuv420p"]))
    anim_gif = FuncAnimation(fig, update, frames=range(0, n_frames, 2), blit=False)
    anim_gif.save(f"{args.out}.gif", writer=PillowWriter(fps=fps // 2))
    update(n_frames - 1)
    fig.savefig(f"{args.out}_final.png", dpi=100)
    print(f"frames={n_frames} ({n_frames / fps:.1f} s) sigma={SIGMA_NM:.1f} nm "
          f"FWHM_PSF={FWHM_PSF_NM:.1f} nm apparent width={width_nm:.1f} nm")


if __name__ == "__main__":
    main()
