# Factory timing — 4DTA00ZA / 4DTA01ZA

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [HTML viewer](../maps/tune_A_vs_B.html) · [Factory A vs B (visual)](../maps/factory-a-vs-b.html) · [Safety](safety.md)

These two tables are the factory **injection-timing look-ups** on the live CM551 dumps. Both calibrations carry the **same decoded grids**. The useful contrast is **transient vs steady-state**, not A vs B.

| | Transient `4DTA00ZA` | Steady-state `4DTA01ZA` |
|---|---|---|
| ITN | `1041` | `103E` |
| Z units | DEG | DEG |
| Shape | 11 × 18 (Y × X) | 11 × 18 |
| X | `4DTA00XA` RPM | `4DTA01XA` RPM (same breakpoints) |
| Y | `4DTA00YA` MM3S (fuel) | `4DTA01YA` MM3S (fuel; **top two breakpoints differ**) |
| A vs B | **same** | **same** |
| ECM A | J90269.06 | J90269.06 |
| ECM B | J90268.04 | J90268.04 |

Decoded values are engineering units after scale/add. They are **not** a flash image and this page is not a write recipe.

Full 29-map viewer (dark HTML): [maps/tune_A_vs_B.html](../maps/tune_A_vs_B.html). Overlay / piggyback context: [quadzilla-vs-factory.md](quadzilla-vs-factory.md).

## Decode scales

`physical = raw × scale + add`. Unsigned 16-bit cells on the wire.

| Item | Scale | Add | Units |
|---|---:|---:|---|
| RPM X (`4DTA00XA` / `4DTA01XA`) | 0.125 | 0 | RPM |
| Fuel Y (`4DTA00YA` / `4DTA01YA`) | 0.0679348 | 0 | MM3S |
| Timing Z (`4DTA00ZA` / `4DTA01ZA`) | 0.1171875 | −60 | DEG |

Example: raw `512` on Z → `512 × 0.1171875 − 60 = 0` DEG. Negative cells in the transient table are real retard, not a decode bug.

Catalog comments still say “17 × 9”. Live axis prefixes on these boxes are **11 × 18**. Prefer the prefix.

## How to read 00 vs 01

Y is **commanded fuel (MM3S)**, not throttle percent. Do not line these rows up with `5DFL`’s 0 / 25 / 50 / 100 throttle axis.

The top of the Y axis is **not shared**:

- Transient Y: … 80.027, **90.014**, **98.03**
- Steady-state Y: … 80.027, **84.986**, **93.478**

Below ~1200 RPM both tables advance several degrees as fuel rises. From **1280 RPM through ~2800 RPM** the **transient** table goes **negative** at mid/high fuel (about −2 to −6.3 DEG). The **steady-state** table stays **positive** in the same RPM band (about +4 to +8 DEG). That hole in `4DTA00ZA` is the factory timing fact that matters if an overlay also tries to advance.

At 3000+ RPM both tables come back positive. The 3800 column repeats the 3250 column on most rows.

## 4DTA00ZA — transient timing (DEG)

Y `4DTA00YA` (MM3S) × X `4DTA00XA` (RPM). A = B.

| Y \ X | 700 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.172 | 1.172 | 1.172 | 0.234 | 0.352 | 0.234 | 1.172 | 1.172 | 1.172 | 2.695 | 3.633 | 4.219 | 4.219 | 4.219 | 4.688 | 5.156 | 5.156 | 5.156 |
| 24.592 | 1.992 | 1.172 | -0.703 | -0.352 | -1.172 | -1.055 | -0.469 | 0.117 | 0.352 | 2.695 | 3.633 | 4.219 | 4.219 | 4.219 | 4.805 | 5.156 | 5.156 | 5.156 |
| 30.774 | 2.227 | 2.227 | 1.523 | -0.352 | -0.469 | -1.406 | -1.523 | -1.875 | -1.289 | -1.289 | -1.172 | -1.289 | -1.289 | -1.289 | -0.703 | 5.156 | 5.156 | 5.156 |
| 43.071 | 2.812 | 3.164 | 4.336 | 0.117 | 0.117 | -0.234 | -1.406 | -2.227 | -1.289 | -1.289 | -1.289 | -1.875 | -2.344 | -3.281 | -2.93 | 2.109 | 3.984 | 3.984 |
| 50 | 2.812 | 5.156 | 9.141 | 9.141 | 1.172 | -0.703 | -1.758 | -2.227 | -2.344 | -2.344 | -2.344 | -3.047 | -4.453 | -5.273 | -5.039 | -0.469 | 3.984 | 3.984 |
| 61.481 | 5.859 | 8.672 | 9.492 | 9.844 | -0.352 | -1.172 | -2.344 | -2.578 | -2.578 | -3.164 | -4.102 | -5.391 | -6.211 | -6.328 | -6.328 | -0.938 | 5.156 | 5.156 |
| 65.014 | 8.789 | 8.672 | 9.727 | 9.844 | -0.234 | -0.82 | -2.461 | -2.812 | -2.93 | -4.102 | -4.922 | -5.859 | -6.328 | -6.328 | -6.328 | -0.469 | 5.742 | 5.742 |
| 73.777 | 8.555 | 9.141 | 10.078 | 10.195 | -0.117 | -1.172 | -2.93 | -3.281 | -3.398 | -4.922 | -6.328 | -6.328 | -6.328 | -5.977 | -5.273 | 1.758 | 6.562 | 6.562 |
| 80.027 | 9.141 | 10.078 | 10.078 | 10.195 | -0.234 | -1.289 | -1.641 | -1.875 | -3.633 | -5.156 | -5.391 | -5.625 | -5.273 | -4.805 | -3.984 | 2.812 | 7.148 | 7.148 |
| 90.014 | 9.727 | 10.078 | 10.078 | 9.844 | 0 | 0 | -0.234 | -0.352 | -0.586 | -0.234 | 0 | 0 | 0.117 | 3.164 | 3.633 | 6.328 | 7.852 | 7.852 |
| 98.03 | 10.078 | 10.078 | 10.078 | 10.078 | 0.117 | 2.109 | 2.461 | 2.227 | 3.164 | 3.75 | 3.633 | 3.516 | 3.867 | 4.219 | 5.039 | 5.859 | 7.852 | 7.852 |

## 4DTA01ZA — steady-state timing (DEG)

Y `4DTA01YA` (MM3S) × X `4DTA01XA` (RPM). A = B.

| Y \ X | 700 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5.977 | 5.977 | 5.977 | 1.992 | 1.992 | 1.992 | 1.992 | 5.039 | 4.805 | 4.57 | 4.57 | 4.805 | 5.039 | 5.156 | 5.156 | 5.156 | 5.156 | 5.156 |
| 24.592 | 5.977 | 5.977 | 5.977 | 1.992 | 1.992 | 1.992 | 1.992 | 5.039 | 4.805 | 4.57 | 4.57 | 4.805 | 5.039 | 5.156 | 5.156 | 5.156 | 5.156 | 5.156 |
| 30.774 | 2.227 | 2.461 | 9.961 | 9.961 | 7.969 | 5.039 | 5.039 | 5.039 | 4.57 | 4.453 | 4.805 | 4.922 | 5.039 | 5.156 | 5.156 | 5.156 | 5.156 | 5.156 |
| 43.071 | 2.812 | 3.516 | 9.961 | 9.961 | 7.969 | 4.57 | 4.453 | 3.984 | 3.75 | 4.453 | 4.805 | 4.922 | 5.039 | 5.156 | 5.156 | 5.156 | 3.984 | 3.984 |
| 50 | 3.047 | 5.156 | 9.961 | 9.961 | 7.969 | 4.805 | 4.805 | 4.336 | 3.867 | 4.453 | 4.805 | 4.922 | 5.039 | 5.156 | 5.156 | 5.156 | 3.984 | 3.984 |
| 61.481 | 7.031 | 9.961 | 9.961 | 9.961 | 7.969 | 5.508 | 5.273 | 4.688 | 4.219 | 4.57 | 4.922 | 5.039 | 5.156 | 5.156 | 5.156 | 5.156 | 5.156 | 5.156 |
| 65.014 | 9.961 | 9.961 | 9.961 | 9.961 | 7.969 | 5.742 | 5.391 | 4.805 | 4.453 | 4.805 | 5.156 | 5.273 | 5.508 | 5.742 | 5.742 | 5.742 | 5.742 | 5.742 |
| 73.777 | 9.961 | 9.961 | 10.078 | 10.195 | 7.969 | 6.562 | 5.625 | 5.156 | 5.156 | 5.508 | 5.977 | 6.211 | 6.445 | 6.562 | 6.562 | 6.562 | 6.562 | 6.562 |
| 80.027 | 9.961 | 10.078 | 10.078 | 10.195 | 7.969 | 6.797 | 5.742 | 5.742 | 5.625 | 5.977 | 6.445 | 6.68 | 6.914 | 7.148 | 7.148 | 7.148 | 7.148 | 7.148 |
| 84.986 | 9.961 | 10.078 | 10.078 | 10.078 | 7.969 | 6.797 | 5.859 | 6.211 | 6.562 | 6.914 | 7.266 | 7.383 | 7.734 | 7.852 | 7.852 | 7.852 | 7.852 | 7.852 |
| 93.478 | 10.078 | 10.078 | 10.078 | 10.781 | 7.969 | 6.797 | 5.859 | 6.211 | 6.562 | 6.914 | 7.266 | 7.383 | 7.734 | 7.852 | 7.852 | 7.852 | 7.852 | 7.852 |

## What this is not

- Not Quadzilla AID 137–141 (“RPM Timing Max”) and not AID 149 (iQuad label “Timing”). Those live on the Adrenaline, not in these KennPars. See [quadzilla-vs-factory.md](quadzilla-vs-factory.md).
- Not a pump-frame recipe. This repository does not document how to command the VP44 on the wire.
- Trailing bytes past the 11 × 18 grid on ITN `1041` differ A vs B in the raw dump (first raw-byte diff at offset 480 of a 512-byte blob). The **decoded table** matches. Do not retune from unused tail bytes.
