# Factory fuel — 5DFL, FLFLTBZA, AFC

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [HTML viewer](../maps/tune_A_vs_B.html) · [Factory A vs B (visual)](../maps/factory-a-vs-b.html) · [Safety](safety.md)

These are the factory **fueling** tables from the two live CM551 dumps. Open this page first if you care about how much fuel the ECM asks for. Timing is in [factory-timing.md](factory-timing.md). Overlay / piggyback: [quadzilla-vs-factory.md](quadzilla-vs-factory.md).

| Cal | ECM code | Cal date | P/N | ROM |
|---|---|---|---|---|
| A | J90269.06 | 062800 | 03942336 | 091197 |
| B | J90268.04 | 102198 | 03942336 | 091197 |

| Map | ITN | Shape | Units | A vs B |
|---|---|---|---|---|
| `5DFL00ZA` transient fuel | `1059` | 4 × 18 | MM3S | **differs** (100% row) |
| `5DFL01ZA` steady-state fuel | `1056` | 4 × 18 | MM3S | **differs** (100% row) |
| `FLFLTBZA` mg/stroke conversion | `8014` | 15 × 15 | MG/S | **same** |
| `AFFLLMZA` AFC boost limiter | `104F` | 14 × 21 (truncated) | MM3S | **differs** (axes and cells) |
| `ATFLLMZA` altitude derate | `10A3` | 4 × 18 | MM3S | **same** (flat 400) |

Decoded values are engineering units after scale/add. They are **not** a flash image and this page is not a write recipe.

Full 29-map viewer: [maps/tune_A_vs_B.html](../maps/tune_A_vs_B.html) (amber cells = A ≠ B). Machine copy: [maps/tune_A_vs_B.json](../maps/tune_A_vs_B.json).

## Decode scales

`physical = raw × scale + add`. Unsigned 16-bit cells on the wire.

| Item | Scale | Add | Units |
|---|---:|---:|---|
| RPM X (`5DFL*XA`, `FLFLESXA`, `AFFLLMXA`, `ATESXA`) | 0.125 | 0 | RPM |
| Fuel Z (`5DFL00ZA` / `5DFL01ZA`) | 0.0679348 | **−800** | MM3S |
| Fuel Z (`AFFLLMZA` / `ATFLLMZA`) | 0.0679348 | 0 | MM3S |
| Fuel Y on timing / conversion (`4DTA*YA`, `FLFLFLYA`) | 0.0679348 | 0 | MM3S |
| Throttle Y (`5DFL00YA` / `5DFL01YA`) | 0.25 | 0 | % |
| Conversion Z (`FLFLTBZA`) | 0.03125 | 0 | MG/S (mg/stroke) |
| Boost / ambient Y (`AFFLLMYA`, `ATAAPRYA`) | 0.01590625 | 0 | INHG |

The **−800** add on 5DFL Z is why a raw zero is not “0 mm³/s” until decode. Tables below are already decoded.

Catalog comments still talk about 17 × 4. Live axis prefixes on these boxes are **4 × 18**. Prefer the prefix. Fuel X starts at **600** RPM (timing X starts at **700**).

## What actually differs

Low-load 5DFL rows (Y = 0 / 25 / 50) **match** A vs B. The **100% (full throttle) row** is the complete, trustworthy cal delta: A is richer in the mid/high RPM columns, especially **2800 and 3000**.

`AFFLLMZA` is a third difference, but the Z dump is **512 of 588 bytes** (256 of 294 cells) and the **RPM and boost axes are not the same** on A and B. Compare cells by physical breakpoint, not by column index. The HTML viewer is index-aligned and will mislead on this map.

`FLFLTBZA` and `ATFLLMZA` match.

## 5DFL00ZA — transient fuel (MM3S)

Y `5DFL00YA` (%) × X `5DFL00XA` (RPM). 4 × 18. ITN `1059`.

### 100% row — A vs B (this is the delta)

| RPM | A | B | A − B |
| --- | --- | --- | --- |
| 600 | 100 | 100 | 0 |
| 800 | 68.275 | 68.275 | 0 |
| 1000 | 68.003 | 68.003 | 0 |
| 1200 | 88.315 | 85.53 | 2.785 |
| 1280 | 97.487 | 97.487 | 0 |
| 1400 | 95.517 | 94.973 | 0.544 |
| 1580 | 94.022 | 94.022 | 0 |
| 1800 | 95.992 | 94.701 | 1.291 |
| 2000 | 98.506 | 95.788 | 2.718 |
| 2200 | 100 | 97.011 | 2.989 |
| 2400 | 101.495 | 98.981 | 2.514 |
| 2500 | 103.397 | 100.815 | 2.582 |
| 2600 | 106.998 | 102.989 | 4.009 |
| 2700 | 109.987 | 106.998 | 2.989 |
| 2800 | 108.968 | 97.011 | 11.957 |
| 3000 | 109.987 | 90.014 | 19.973 |
| 3250 | 87.025 | 87.025 | 0 |
| 3800 | 0 | 0 | 0 |

Largest gaps: **3000 RPM** A is **+19.973** MM3S vs B (109.987 vs 90.014); **2800** is **+11.957** (108.968 vs 97.011). Several mid-RPM cells are 2–4 MM3S richer on A. 600 / 800 / 1000 / 1280 / 1580 / 3250 / 3800 match. The 3800 column is **0** on both (unused high breakpoint, not a driveable fueling point).

### Full grid, calibration A (J90269.06)

| Y \ X | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 8.968 | 4.008 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25 | 33.22 | 28.261 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 0 |
| 50 | 57.473 | 52.514 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 0 |
| 100 | 100 | 68.275 | 68.003 | 88.315 | 97.487 | 95.517 | 94.022 | 95.992 | 98.506 | 100 | 101.495 | 103.397 | 106.998 | 109.987 | 108.968 | 109.987 | 87.025 | 0 |

### Full grid, calibration B (J90268.04)

| Y \ X | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 8.968 | 4.008 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25 | 33.22 | 28.261 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 23.234 | 0 |
| 50 | 57.473 | 52.514 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 47.487 | 0 |
| 100 | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 97.011 | 90.014 | 87.025 | 0 |

Rows Y = 0 / 25 / 50 are identical A vs B. Y = 25 holds **23.234** from 1000 through 3250 RPM; Y = 50 holds **47.487** in that same span.

## 5DFL01ZA — steady-state fuel (MM3S)

Y `5DFL01YA` (%) × X `5DFL01XA` (RPM). 4 × 18. ITN `1056`.

Same story as transient, with a slightly leaner 100% row on both boxes and a **larger** A-vs-B gap at 2800–3000.

### 100% row — A vs B

| RPM | A | B | A − B |
| --- | --- | --- | --- |
| 600 | 100 | 100 | 0 |
| 800 | 67.527 | 67.527 | 0 |
| 1000 | 68.003 | 68.003 | 0 |
| 1200 | 88.315 | 84.987 | 3.328 |
| 1280 | 96.468 | 95.517 | 0.951 |
| 1400 | 94.633 | 94.022 | 0.611 |
| 1580 | 94.973 | 93.207 | 1.766 |
| 1800 | 95.177 | 93.818 | 1.359 |
| 2000 | 97.011 | 93.614 | 3.397 |
| 2200 | 98.03 | 93.275 | 4.755 |
| 2400 | 99.525 | 94.973 | 4.552 |
| 2500 | 100.68 | 95.517 | 5.163 |
| 2600 | 104.008 | 96.468 | 7.54 |
| 2700 | 107.473 | 100.272 | 7.201 |
| 2800 | 106.998 | 94.022 | 12.976 |
| 3000 | 109.987 | 87.296 | 22.691 |
| 3250 | 87.025 | 87.025 | 0 |
| 3800 | 0 | 0 | 0 |

Largest gaps: **3000 RPM** A is **+22.691** MM3S vs B (109.987 vs 87.296); **2800** is **+12.976** (106.998 vs 94.022). Part-load rows match.

### Full grid, calibration A (J90269.06)

| Y \ X | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 8.968 | 4.008 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25 | 33.017 | 27.989 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 0 |
| 50 | 56.998 | 51.97 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 0 |
| 100 | 100 | 67.527 | 68.003 | 88.315 | 96.468 | 94.633 | 94.973 | 95.177 | 97.011 | 98.03 | 99.525 | 100.68 | 104.008 | 107.473 | 106.998 | 109.987 | 87.025 | 0 |

### Full grid, calibration B (J90268.04)

| Y \ X | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 8.968 | 4.008 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25 | 33.017 | 27.989 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 23.03 | 0 |
| 50 | 56.998 | 51.97 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 47.011 | 0 |
| 100 | 100 | 67.527 | 68.003 | 84.987 | 95.517 | 94.022 | 93.207 | 93.818 | 93.614 | 93.275 | 94.973 | 95.517 | 96.468 | 100.272 | 94.022 | 87.296 | 87.025 | 0 |

## FLFLTBZA — fuel units → mg/stroke (MG/S)

Y `FLFLFLYA` (MM3S) × X `FLFLESXA` (RPM). 15 × 15. ITN `8014`. **A = B.**

This is a **conversion / density-style** table, not the throttle-to-fuel request. UDC/KennPar name overlap is why tuners already know the string. Changing it without changing 5DFL is a different kind of edit than raising the 100% fuel row.

| Y \ X | 200 | 400 | 600 | 700 | 775 | 800 | 1200 | 1600 | 2000 | 2300 | 2500 | 2700 | 3000 | 3200 | 3500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 19.973 | 24.9688 | 24.9688 | 24.9688 | 22.7188 | 21.0312 | 19.625 | 18.5938 | 18.8125 | 19.25 | 19.4062 | 19.6875 | 19.5 | 21.375 | 21.25 | 21.25 |
| 40.014 | 40 | 40 | 39.2812 | 39.2812 | 39.2812 | 39.2812 | 37.1562 | 37.625 | 38.5 | 38.8125 | 39.375 | 39 | 42.75 | 42.5 | 42.5 |
| 80.027 | 80 | 80 | 78.5312 | 78.5312 | 78.5312 | 78.5312 | 74.3438 | 75.25 | 77 | 77.625 | 78.7188 | 78.0312 | 85.4688 | 85.0312 | 85.0312 |
| 119.973 | 120 | 120 | 117.8125 | 117.8125 | 117.8125 | 117.8125 | 111.5 | 112.875 | 115.5 | 116.4688 | 118.0938 | 117.0312 | 128.2188 | 127.5312 | 127.5312 |
| 150 | 150 | 150 | 147.25 | 147.25 | 147.25 | 147.25 | 139.375 | 141.125 | 144.375 | 145.5625 | 147.5938 | 146.3125 | 160.2812 | 159.4062 | 159.4062 |
| 159.986 | 160 | 160 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 |
| 169.973 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 |
| 180.027 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 |
| 190.014 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 |
| 200 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 |
| 209.986 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 |
| 219.973 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 |
| 230.027 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 |
| 240.014 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 |

Below ~160 MM3S the table still varies with RPM (a dip through 1200–2700, then a bump at 3000). From Y = 159.986 upward the rows are **flat across RPM** (167, 175, 183, … 234).

## AFFLLMZA — AFC limiter (MM3S), truncated

ITN `104F`. Declared **14 × 21**. Z ITN returned **512 of 588 bytes** (256 of 294 cells). Last complete row is Y index 11; Y index 12 has four cells; Y index 13 is empty. **Do not treat the 14 × 21 grid as fully known.**

AFC look-up: fueling **limit** vs **boost (INHG) × RPM**. This is the factory smoke/boost limiter, not the 5DFL request.

### Axes differ A vs B

Do not compare column 2 of A to column 2 of B. Those are different RPM.

**RPM X `AFFLLMXA`**

| | Breakpoints |
|---|---|
| A | 600, **700**, 800, 1000, 1200, 1280, 1400, 1580, 1800, 2000, 2200, 2400, 2500, 2600, 2700, 2800, 3000, 3250, 3800, 4000, 4200 |
| B | 600, 800, 1000, 1200, 1280, 1400, 1580, 1800, 2000, 2200, 2400, 2500, 2600, 2700, 2800, 3000, 3250, 3800, 4000, 4200, **4500** |

A has **700**; B has **4500** instead.

**Boost Y `AFFLLMYA` (INHG)**

| | Breakpoints |
|---|---|
| A | 0, 1.00, 2.00, 3.01, 4.99, 10.01, 15.00, 19.99, **25.00**, **30.00**, 34.99, 40.00, 44.00, 48.01 |
| B | 0, 1.00, 2.00, 3.01, 4.99, 10.01, 15.00, 19.99, 34.99, 40.00, 44.00, 48.01, **100.00**, **110.01** |

A samples 25 and 30 inHg. B skips those and adds 100 / 110 inHg (well above a stock Dodge boost range — leftover / unused tail).

### Same-breakpoint slices (not index-aligned)

Shared RPM on Y = 0 INHG (zero boost). A is the richer limiter everywhere this dump can compare:

| RPM | A | B | A − B |
| --- | --- | --- | --- |
| 600 | 119.973 | 100 | 19.973 |
| 800 | 130.027 | 66.372 | 63.655 |
| 1000 | 73.573 | 63.451 | 10.122 |
| 1200 | 73.573 | 63.519 | 10.054 |
| 1280 | 73.573 | 44.973 | 28.6 |
| 1400 | 73.573 | 44.973 | 28.6 |
| 1580 | 73.573 | 44.973 | 28.6 |
| 1800 | 73.573 | 44.973 | 28.6 |
| 2000 | 73.573 | 44.973 | 28.6 |
| 2200 | 73.573 | 44.973 | 28.6 |
| 2400 | 73.573 | 44.973 | 28.6 |
| 2500 | 73.573 | 44.973 | 28.6 |
| 2600 | 73.573 | 44.973 | 28.6 |
| 2700 | 73.573 | 44.973 | 28.6 |
| 2800 | 73.573 | 44.973 | 28.6 |
| 3000 | 73.573 | 44.973 | 28.6 |
| 3250 | 72.147 | 44.973 | 27.174 |
| 3800 | 72.147 | 44.973 | 27.174 |

At zero boost, B falls to a **44.973** MM3S ceiling from 1280 RPM up. A holds **73.573** (then **72.147** at 3250+). That is a real AFC difference, independent of 5DFL.

Shared RPM on Y ≈ 19.99 INHG (~10 PSI — still a light-boost row, not the 14×21 peak):

| RPM | A | B | A − B |
| --- | --- | --- | --- |
| 600 | 119.973 | 100 | 19.973 |
| 800 | 140.897 | 100.747 | 40.15 |
| 1000 | 164.334 | 97.215 | 67.119 |
| 1200 | 164.334 | 99.321 | 65.013 |
| 1280 | 164.334 | 108.56 | 55.774 |
| 1400 | 164.334 | 106.318 | 58.016 |
| 1580 | 164.334 | 97.011 | 67.323 |
| 1800 | 164.334 | 88.383 | 75.951 |
| 2000 | 164.334 | 86.277 | 78.057 |
| 2200 | 164.334 | 87.228 | 77.106 |
| 2400 | 164.334 | 88.791 | 75.543 |
| 2500 | 164.334 | 88.859 | 75.475 |
| 2600 | 164.334 | 86.141 | 78.193 |
| 2700 | 164.334 | 86.141 | 78.193 |
| 2800 | 164.334 | 78.465 | 85.869 |
| 3000 | 164.334 | 75.543 | 88.791 |
| 3250 | 170.109 | 72.962 | 97.147 |
| 3800 | 170.109 | 75 | 95.109 |

At this boost row A sits near **164** MM3S across most of the RPM axis (higher than any 5DFL 100% cell). B is lower and RPM-shaped. So on the sampled complete rows, **A’s AFC ceiling is well above 5DFL**; **B’s AFC is much tighter at low boost**.

The HTML page still shows index-aligned A vs B (A column 1 = 700 RPM vs B column 1 = 800 RPM). Use this markdown or re-align by breakpoint. Remaining cells: [HTML AFFLLMZA section](../maps/tune_A_vs_B.html#AFFLLMZA).

## ATFLLMZA — altitude derate (MM3S)

ITN `10A3`. 4 × 18. Y `ATAAPRYA` (INHG ambient) × X `ATESXA` (RPM). **A = B.**

Every decoded cell is **400** MM3S:

| Y \ X | 0 | 296 | 500 | 653 | 826 | 948 | 1071 | 1203 | 1295 | 1397 | 1499 | 1601 | 1805 | 1947 | 2100 | 2498 | 2600 | 3000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 |
| 18.9284 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 |
| 20.5509 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 |
| 30.54 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 | 400 |

400 is far above the 5DFL 100% row (~88–110). On these two boxes the altitude table is a **high ceiling**, not an active derate relative to the fuel request. Adrenaline does not need to “match” a factory altitude cut that is not doing any cutting here.

## Using this with an overlay

If a piggyback already adds fuel (Quadzilla AID 85 stretch, boost-percent curves, …), stacking a richer 5DFL 100% row on top of that is **more fuel than either change alone**. A is already the richer factory 5DFL. Harmonize notes: [quadzilla-vs-factory.md](quadzilla-vs-factory.md). This repository will not tell you how to program an ECM.
