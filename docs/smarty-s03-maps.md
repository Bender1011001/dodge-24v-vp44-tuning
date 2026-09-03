# Smarty S03 maps vs factory CM551

Owner-facing decode of **UDC Pro RT year-stock `.dat` files** (already decrypted in the lab) compared to the live KennPar dumps:

- Factory **A** `J90269.06` cal `062800` PN `03942336`
- Factory **B** `J90268.04` cal `102198` PN `03942336`

This page is **read-only documentation**. It is not a flash kit and does not describe how to program a Smarty or an ECM.

## Inventory (actual filenames)

There are **no** lab files named stock / +30 / +60 / race. Those labels do not appear on the S03 media we have. What exists:

### 1. UDC Pro RT stock database (`db/*.dat`)

Thirty year/transmission calibrations. Stem pattern `YYYYoPU{Aut|Man}xxJ`. The two-digit `xx` is a UDC family code, **not** a Smarty SW number and **not** advertised HP.

| File | Year | Trans | Family code | Layout flash | IQ RPM axis score | Role |
|---|---|---|---|---|---|---|
| `19980PUAut54J` | 1998.5-99 | Aut | 54 | `0x00807A7A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19980PUAut74J` | 1998.5-99 | Aut | 74 | `0x00807A7A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19980PUMan44J` | 1998.5-99 | Man | 44 | `0x00807A7A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19980PUMan64J` | 1998.5-99 | Man | 64 | `0x00807A7A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19990PUAut06J` | 1999 | Aut | 06 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19990PUAut76J` | 1999 | Aut | 76 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19990PUMan86J` | 1999 | Man | 86 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `19990PUMan96J` | 1999 | Man | 96 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20000PUAut04J` | 2000 | Aut | 04 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20000PUAut94J` | 2000 | Aut | 94 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20000PUMan14J` | 2000 | Man | 14 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20000PUMan24J` | 2000 | Man | 24 | `0x00807A8C` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUAut08J` | 2000.5 | Aut | 08 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUAut57J` | 2000.5 | Aut | 57 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUMan16J` | 2000.5 | Man | 16 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUMan27J` | 2000.5 | Man | 27 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUMan35J` | 2000.5 | Man | 35 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20005PUMan46J` | 2000.5 | Man | 46 | `0x008079EC` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUAut76J` | 2001 | Aut | 76 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUAut86J` | 2001 | Aut | 86 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUMan05J` | 2001 | Man | 05 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUMan15J` | 2001 | Man | 15 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUMan25J` | 2001 | Man | 25 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20010PUMan95J` | 2001 | Man | 95 | `0x00807A0A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUAut42J` | 2002 | Aut | 42 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUAut52J` | 2002 | Aut | 52 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUMan61J` | 2002 | Man | 61 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUMan71J` | 2002 | Man | 71 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUMan83J` | 2002 | Man | 83 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |
| `20020PUMan93J` | 2002 | Man | 93 | `0x00807A2A` | 1.929 | UDC **stock** cal (not SW0–9) |

1998.5–99 (this truck’s ROM family `091197` / P/N `03942336`) is four files: `19980PUMan44J`, `19980PUMan64J`, `19980PUAut54J`, `19980PUAut74J`.

### 2. Handheld `.Smt` (CaTCHER slots = software families)

| File | Bytes | What it is |
|---|---|---|
| `S03V126CDR12A.Smt` | 4 313 006 | S03 v1.26 handheld image. **Five** CaTCHER slots after FLASH_KEY decode. |
| `SmtEV1_22D107A.smt` … `D407A.smt` | ~6 MB each | S03 v1.22 variants. Lab notes: **zero** CaTCHER slots. |
| `Stock_demo.smarty` / `Modified_demo.smarty` | 7 856 each | Official SmartyUDCsw demo documents, not year `.dat` maps. |

### 3. Published SW0–SW9 (manual / Tome site — not filenames)

| SW | Title (Tome) | What the lab can say in KennPar units |
|---|---|---|
| 0 | Half power / no-smoke | Maps to SMT slot **L0**. Not stock. **No** FLFL/4DTA/5DFL grid recovered from the slot. |
| 1 | Fuel saver | Timing-heavy; **not** a sixth SMT slot (U2 knob defaults). |
| 2 | Fuel + boost fooling | No published HP. Not a raw KennPar overlay in the `.dat`. |
| 3 | SW2 + timing | Odd SW adds timing via on-device knob. |
| 4–9 | CaTCHER | Even = no extra timing (timing-box users); odd = added timing. SMT slots L2/L3/L4 are the fuel/boost **families**, not ten copies of 4DTA. |

## Method

- **Plaintext source:** `db/*.dat.plain` from the already-recovered UDC native decoder (`LIB_0203` `PCGet` / `tools/udc_db_decrypt.py`). XOR-key guessing stays **frozen**; this pass does not brute keys.
- **Layout:** decrypted cal image, **u16 big-endian**, same as live KennPar. Axes start with a 2-byte BE length (byte count of the point list). 1998 IQ RPM-axis score: **1.929**.
- **Scales/add (Chr0000 meta, same as live ECM decode):** IQ `× 0.03125`; RPM `× 0.125`; 5DFL `× 0.0679348 − 800` MM3/s; 4DTA `× 0.1171875 − 60` deg.
- **Factory grids:** `maps/tune_A_vs_B.json` (ReadByNTN, not a flash image).
- **Not used:** `analyze_s03_udcgrid.py` rot-254-of-header (false path once `.plain` exists).

## What actually changes (1998 UDC stock vs factory)

The four 1998 files decode to **valid** 15×15 IQ, 11×18 timing, and 4×18 5D fuel tables. They are **stock UDC copies**, not Smarty power levels. Against the live boxes:

| 1998 file | FLFL vs A (nΔ / max) | FLFL vs B | 4DTA00 vs A | 4DTA00 vs B | 5DFL00 vs A | 5DFL00 vs B |
|---|---|---|---|---|---|---|
| `19980PUAut54J` | 69/225 max 11.8438 | 69/225 max 11.8438 | 198/198 max 5.0387 | 198/198 max 5.0387 | 52/72 max 77.9894 | 52/72 max 77.9894 |
| `19980PUAut74J` | 69/225 max 11.8438 | 69/225 max 11.8438 | 198/198 max 5.0387 | 198/198 max 5.0387 | 52/72 max 77.9894 | 52/72 max 77.9894 |
| `19980PUMan44J` | 69/225 max 11.8438 | 69/225 max 11.8438 | 198/198 max 5.0387 | 198/198 max 5.0387 | 12/72 max 12.9752 | 3/72 max 12.9752 |
| `19980PUMan64J` | equal | equal | 198/198 max 5.0387 | 198/198 max 5.0387 | 12/72 max 12.9752 | 3/72 max 12.9752 |

### Headline

- **Aut54 = Aut74** on IQ, timing, and 5D fuel (one Aut stock, two filenames).
- **Man44 = Man64** on `4DTA` and `5DFL`. They differ **only** in `FLFLTBZA`. **Man64 IQ equals the live factory conversion table** (A = B on that map). Man44 / Aut share a second IQ table (69 / 225 cells, mean +3.7 mg/stroke vs factory).
- **5DFL00 manual WOT:** matches factory **B** through 2700 RPM. The only WOT splits vs B are 2800 RPM **+3.0 MM3/s**, 3000 **+10.0**, 3250 **+13.0**. vs A the same row is leaner from 1200–3000 (2000 RPM **−2.7**, 2800 **−9.0**).
- **5DFL00 auto WOT:** a different map. Midrange is leaner than both live boxes; 3800 RPM is **78 MM3/s** vs factory **0** (the live dumps zero that column).
- **4DTA vs live (A = B):** UDC stock is **more retarded**. Peak-load 2000 RPM: factory 3.16°, Man 1.99° (Δ **−1.17°**), Aut 0.59° (Δ **−2.58°**). 2800 RPM: factory 5.04°, Man 3.87°, Aut 2.34°. Mean cell Δ about **−1.3°** transient / **−3.5°** steady-state.
- None of these four files is a Smarty SW0–SW9 overlay.

### 1998 Aut vs Man (not independent power levels)

- `19980PUAut54J` vs `19980PUAut74J` — FLFLTBZA: equal, 4DTA00ZA: equal, 4DTA01ZA: equal, 5DFL00ZA: equal, 5DFL01ZA: equal
- `19980PUAut54J` vs `19980PUMan44J` — FLFLTBZA: equal, 4DTA00ZA: 173 cells, 4DTA01ZA: 9 cells, 5DFL00ZA: 52 cells, 5DFL01ZA: 52 cells
- `19980PUAut54J` vs `19980PUMan64J` — FLFLTBZA: 69 cells, 4DTA00ZA: 173 cells, 4DTA01ZA: 9 cells, 5DFL00ZA: 52 cells, 5DFL01ZA: 52 cells
- `19980PUAut74J` vs `19980PUMan44J` — FLFLTBZA: equal, 4DTA00ZA: 173 cells, 4DTA01ZA: 9 cells, 5DFL00ZA: 52 cells, 5DFL01ZA: 52 cells
- `19980PUAut74J` vs `19980PUMan64J` — FLFLTBZA: 69 cells, 4DTA00ZA: 173 cells, 4DTA01ZA: 9 cells, 5DFL00ZA: 52 cells, 5DFL01ZA: 52 cells
- `19980PUMan44J` vs `19980PUMan64J` — FLFLTBZA: 69 cells, 4DTA00ZA: equal, 4DTA01ZA: equal, 5DFL00ZA: equal, 5DFL01ZA: equal

## `19980PUAut54J` (Aut, family 54)

Layout `0x00807A7A`. UDC **stock** calibration.

### FLFLTBZA (MG/S) [15, 15]

Axes: X matches factory; Y matches factory.

- vs factory A: **69 / 225 cells differ**, max |Δ| 11.8438 mean Δ 3.6748
- vs factory B: **69 / 225 cells differ**, max |Δ| 11.8438 mean Δ 3.6748

IQ max cell: UDC 234.0 mg/stroke; factory 234.0 (A=B on this map).

UDC grid (mg/stroke):

| Y \ X | 200 | 400 | 600 | 700 | 775 | 800 | 1200 | 1600 | 2000 | 2300 | 2500 | 2700 | 3000 | 3200 | 3500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 19.97 | 25.47 | 25.47 | 25.47 | 23.31 | 21.66 | 20.59 | 19.91 | 20.31 | 20.84 | 20.78 | 20.56 | 20.88 | 20.94 | 21.41 | 21.41 |
| 40.01 | 40 | 40 | 41.16 | 41.16 | 41.16 | 41.16 | 39.81 | 40.62 | 41.66 | 41.59 | 41.12 | 41.72 | 41.88 | 42.81 | 42.81 |
| 80.03 | 80 | 80 | 82.34 | 82.34 | 82.34 | 82.34 | 79.62 | 81.28 | 83.31 | 83.16 | 82.25 | 83.44 | 83.78 | 85.59 | 85.59 |
| 119.97 | 120 | 120 | 123.5 | 123.5 | 123.5 | 123.5 | 119.44 | 121.94 | 124.97 | 124.75 | 123.38 | 125.19 | 125.66 | 128.41 | 128.41 |
| 150 | 150 | 150 | 154.38 | 154.38 | 154.38 | 154.38 | 149.31 | 152.41 | 156.22 | 155.94 | 154.25 | 156.47 | 157.09 | 160.5 | 160.5 |
| 159.99 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 |
| 169.97 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 |
| 180.03 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 |
| 190.01 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 |
| 200 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 |
| 209.99 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 |
| 219.97 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 |
| 230.03 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 |
| 240.01 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 |

### 4DTA00ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.3151
- vs factory B: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.3151

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 0.586 | 3.164 | -2.578 |
| 2800 | 2.344 | 5.039 | -2.695 |
| 3000 | 3.398 | 5.859 | -2.461 |

Peak-load row span UDC 0.3516 … 9.6094 deg; factory 0.117 … 10.078 deg.

### 4DTA01ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.5387
- vs factory B: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.5387

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 0.586 | 6.562 | -5.976 |
| 2800 | 2.344 | 7.852 | -5.508 |
| 3000 | 3.398 | 7.852 | -4.454 |

Peak-load row span UDC 0.3516 … 9.9609 deg; factory 5.859 … 10.781 deg.

### 5DFL00ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **52 / 72 cells differ**, max |Δ| 77.9894 mean Δ -2.0056
- vs factory B: **52 / 72 cells differ**, max |Δ| 77.9894 mean Δ -0.9604

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 90.014 | 68.478 | 66.984 | 73.03 | 83.968 | 86.481 | 87.5 | 89.878 | 93.478 | 95.177 | 97.283 | 100 | 102.378 | 105.027 | 101.97 | 108.288 | 77.989 | 77.989 |
| factory | 100 | 68.275 | 68.003 | 88.315 | 97.487 | 95.517 | 94.022 | 95.992 | 98.506 | 100 | 101.495 | 103.397 | 106.998 | 109.987 | 108.968 | 109.987 | 87.025 | 0 |
| Δ | -9.986 | 0.203 | -1.019 | -15.285 | -13.519 | -9.036 | -6.522 | -6.114 | -5.028 | -4.823 | -4.212 | -3.397 | -4.62 | -4.96 | -6.998 | -1.699 | -9.036 | 77.989 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 90.014 | 68.478 | 66.984 | 73.03 | 83.968 | 86.481 | 87.5 | 89.878 | 93.478 | 95.177 | 97.283 | 100 | 102.378 | 105.027 | 101.97 | 108.288 | 77.989 | 77.989 |
| factory | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 97.011 | 90.014 | 87.025 | 0 |
| Δ | -9.986 | 0.203 | -1.019 | -12.5 | -13.519 | -8.492 | -6.522 | -4.823 | -2.309 | -1.834 | -1.698 | -0.815 | -0.611 | -1.971 | 4.959 | 18.274 | -9.036 | 77.989 |

### 5DFL01ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **52 / 72 cells differ**, max |Δ| 77.9894 mean Δ -1.8002
- vs factory B: **52 / 72 cells differ**, max |Δ| 77.9894 mean Δ -0.3331

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 90.014 | 66.984 | 66.984 | 72.487 | 80.503 | 81.794 | 84.987 | 87.5 | 92.324 | 94.022 | 96.807 | 98.71 | 102.514 | 104.891 | 101.97 | 108.288 | 77.989 | 77.989 |
| factory | 100 | 67.527 | 68.003 | 88.315 | 96.468 | 94.633 | 94.973 | 95.177 | 97.011 | 98.03 | 99.525 | 100.68 | 104.008 | 107.473 | 106.998 | 109.987 | 87.025 | 0 |
| Δ | -9.986 | -0.543 | -1.019 | -15.828 | -15.965 | -12.839 | -9.986 | -7.677 | -4.687 | -4.008 | -2.718 | -1.971 | -1.494 | -2.582 | -5.028 | -1.699 | -9.036 | 77.989 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 90.014 | 66.984 | 66.984 | 72.487 | 80.503 | 81.794 | 84.987 | 87.5 | 92.324 | 94.022 | 96.807 | 98.71 | 102.514 | 104.891 | 101.97 | 108.288 | 77.989 | 77.989 |
| factory | 100 | 67.527 | 68.003 | 84.987 | 95.517 | 94.022 | 93.207 | 93.818 | 93.614 | 93.275 | 94.973 | 95.517 | 96.468 | 100.272 | 94.022 | 87.296 | 87.025 | 0 |
| Δ | -9.986 | -0.543 | -1.019 | -12.5 | -15.014 | -12.228 | -8.22 | -6.318 | -1.29 | 0.747 | 1.834 | 3.193 | 6.046 | 4.619 | 7.948 | 20.992 | -9.036 | 77.989 |


## `19980PUAut74J` (Aut, family 74)

Decoded grids are **identical** to `19980PUAut54J`. See that section for tables.

## `19980PUMan44J` (Man, family 44)

Layout `0x00807A7A`. UDC **stock** calibration.

### FLFLTBZA (MG/S) [15, 15]

Axes: X matches factory; Y matches factory.

- vs factory A: **69 / 225 cells differ**, max |Δ| 11.8438 mean Δ 3.6748
- vs factory B: **69 / 225 cells differ**, max |Δ| 11.8438 mean Δ 3.6748

IQ max cell: UDC 234.0 mg/stroke; factory 234.0 (A=B on this map).

UDC grid (mg/stroke):

| Y \ X | 200 | 400 | 600 | 700 | 775 | 800 | 1200 | 1600 | 2000 | 2300 | 2500 | 2700 | 3000 | 3200 | 3500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 19.97 | 25.47 | 25.47 | 25.47 | 23.31 | 21.66 | 20.59 | 19.91 | 20.31 | 20.84 | 20.78 | 20.56 | 20.88 | 20.94 | 21.41 | 21.41 |
| 40.01 | 40 | 40 | 41.16 | 41.16 | 41.16 | 41.16 | 39.81 | 40.62 | 41.66 | 41.59 | 41.12 | 41.72 | 41.88 | 42.81 | 42.81 |
| 80.03 | 80 | 80 | 82.34 | 82.34 | 82.34 | 82.34 | 79.62 | 81.28 | 83.31 | 83.16 | 82.25 | 83.44 | 83.78 | 85.59 | 85.59 |
| 119.97 | 120 | 120 | 123.5 | 123.5 | 123.5 | 123.5 | 119.44 | 121.94 | 124.97 | 124.75 | 123.38 | 125.19 | 125.66 | 128.41 | 128.41 |
| 150 | 150 | 150 | 154.38 | 154.38 | 154.38 | 154.38 | 149.31 | 152.41 | 156.22 | 155.94 | 154.25 | 156.47 | 157.09 | 160.5 | 160.5 |
| 159.99 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 | 167 |
| 169.97 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 | 175 |
| 180.03 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 | 183 |
| 190.01 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 | 191 |
| 200 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 | 199 |
| 209.99 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 | 207 |
| 219.97 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 | 215 |
| 230.03 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 | 224 |
| 240.01 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 | 234 |

### 4DTA00ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.4299
- vs factory B: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.4299

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 1.992 | 3.164 | -1.172 |
| 2800 | 3.867 | 5.039 | -1.172 |
| 3000 | 3.398 | 5.859 | -2.461 |

Peak-load row span UDC -1.0547 … 8.9062 deg; factory 0.117 … 10.078 deg.

### 4DTA01ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.4394
- vs factory B: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.4394

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 3.164 | 6.562 | -3.398 |
| 2800 | 5.039 | 7.852 | -2.813 |
| 3000 | 3.398 | 7.852 | -4.454 |

Peak-load row span UDC 2.2266 … 9.9609 deg; factory 5.859 … 10.781 deg.

### 5DFL00ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **12 / 72 cells differ**, max |Δ| 12.9752 mean Δ -2.3666
- vs factory B: **3 / 72 cells differ**, max |Δ| 12.9752 mean Δ 8.6502

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 68.275 | 68.003 | 88.315 | 97.487 | 95.517 | 94.022 | 95.992 | 98.506 | 100 | 101.495 | 103.397 | 106.998 | 109.987 | 108.968 | 109.987 | 87.025 | 0 |
| Δ | 0 | 0 | 0 | -2.785 | 0 | -0.544 | 0 | -1.291 | -2.718 | -2.989 | -2.514 | -2.582 | -4.009 | -2.989 | -8.968 | -9.987 | 12.975 | 0 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 97.011 | 90.014 | 87.025 | 0 |
| Δ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -0.001 | 2.989 | 9.986 | 12.975 | 0 |

### 5DFL01ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **15 / 72 cells differ**, max |Δ| 12.9752 mean Δ -0.6839
- vs factory B: **15 / 72 cells differ**, max |Δ| 12.9752 mean Δ 4.4021

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 67.527 | 68.003 | 88.315 | 96.468 | 94.633 | 94.973 | 95.177 | 97.011 | 98.03 | 99.525 | 100.68 | 104.008 | 107.473 | 106.998 | 109.987 | 87.025 | 0 |
| Δ | 0 | 0.748 | 0 | -2.785 | 1.019 | 0.34 | -0.951 | -0.476 | -1.223 | -1.019 | -0.544 | 0.135 | -1.019 | -0.475 | -6.998 | -9.987 | 12.975 | 0 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 67.527 | 68.003 | 84.987 | 95.517 | 94.022 | 93.207 | 93.818 | 93.614 | 93.275 | 94.973 | 95.517 | 96.468 | 100.272 | 94.022 | 87.296 | 87.025 | 0 |
| Δ | 0 | 0.748 | 0 | 0.543 | 1.97 | 0.951 | 0.815 | 0.883 | 2.174 | 3.736 | 4.008 | 5.298 | 6.521 | 6.725 | 5.978 | 12.704 | 12.975 | 0 |


## `19980PUMan64J` (Man, family 64)

Layout `0x00807A7A`. UDC **stock** calibration.

### FLFLTBZA (MG/S) [15, 15]

Axes: X matches factory; Y matches factory.

- vs factory A: **equal**
- vs factory B: **equal**

IQ max cell: UDC 234.0 mg/stroke; factory 234.0 (A=B on this map).

### 4DTA00ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.4299
- vs factory B: **198 / 198 cells differ**, max |Δ| 5.0387 mean Δ -1.4299

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 1.992 | 3.164 | -1.172 |
| 2800 | 3.867 | 5.039 | -1.172 |
| 3000 | 3.398 | 5.859 | -2.461 |

Peak-load row span UDC -1.0547 … 8.9062 deg; factory 0.117 … 10.078 deg.

### 4DTA01ZA (DEG) [11, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.4394
- vs factory B: **157 / 198 cells differ**, max |Δ| 6.5628 mean Δ -3.4394

Peak-load row (last Y), selected RPM (deg):

| RPM | UDC | factory A/B (timing A=B) | Δ |
|---|---|---|---|
| 2000 | 3.164 | 6.562 | -3.398 |
| 2800 | 5.039 | 7.852 | -2.813 |
| 3000 | 3.398 | 7.852 | -4.454 |

Peak-load row span UDC 2.2266 … 9.9609 deg; factory 5.859 … 10.781 deg.

### 5DFL00ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **12 / 72 cells differ**, max |Δ| 12.9752 mean Δ -2.3666
- vs factory B: **3 / 72 cells differ**, max |Δ| 12.9752 mean Δ 8.6502

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 68.275 | 68.003 | 88.315 | 97.487 | 95.517 | 94.022 | 95.992 | 98.506 | 100 | 101.495 | 103.397 | 106.998 | 109.987 | 108.968 | 109.987 | 87.025 | 0 |
| Δ | 0 | 0 | 0 | -2.785 | 0 | -0.544 | 0 | -1.291 | -2.718 | -2.989 | -2.514 | -2.582 | -4.009 | -2.989 | -8.968 | -9.987 | 12.975 | 0 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 97.011 | 90.014 | 87.025 | 0 |
| Δ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -0.001 | 2.989 | 9.986 | 12.975 | 0 |

### 5DFL01ZA (MM3S) [4, 18]

Axes: X matches factory; Y matches factory.

- vs factory A: **15 / 72 cells differ**, max |Δ| 12.9752 mean Δ -0.6839
- vs factory B: **15 / 72 cells differ**, max |Δ| 12.9752 mean Δ 4.4021

WOT row (Y=100%) vs A and vs B:

vs A:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 67.527 | 68.003 | 88.315 | 96.468 | 94.633 | 94.973 | 95.177 | 97.011 | 98.03 | 99.525 | 100.68 | 104.008 | 107.473 | 106.998 | 109.987 | 87.025 | 0 |
| Δ | 0 | 0.748 | 0 | -2.785 | 1.019 | 0.34 | -0.951 | -0.476 | -1.223 | -1.019 | -0.544 | 0.135 | -1.019 | -0.475 | -6.998 | -9.987 | 12.975 | 0 |

vs B:

| RPM | 600 | 800 | 1000 | 1200 | 1280 | 1400 | 1580 | 1800 | 2000 | 2200 | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3250 | 3800 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDC | 100 | 68.275 | 68.003 | 85.53 | 97.487 | 94.973 | 94.022 | 94.701 | 95.788 | 97.011 | 98.981 | 100.815 | 102.989 | 106.998 | 100 | 100 | 100 | 0 |
| factory | 100 | 67.527 | 68.003 | 84.987 | 95.517 | 94.022 | 93.207 | 93.818 | 93.614 | 93.275 | 94.973 | 95.517 | 96.468 | 100.272 | 94.022 | 87.296 | 87.025 | 0 |
| Δ | 0 | 0.748 | 0 | 0.543 | 1.97 | 0.951 | 0.815 | 0.883 | 2.174 | 3.736 | 4.008 | 5.298 | 6.521 | 6.725 | 5.978 | 12.704 | 12.975 | 0 |


## 5DFL in the `.dat`

5D fuel **is** present in the UDC year `.dat` (both `5DFL00ZA` / `5DFL01ZA`, 4×18). Smarty **handheld software levels** are a different container: the `.Smt` does not carry these tables as KennPar grids. If a tuner only overlays IQ+timing in UDC, that is a UDC-document behavior — the **stock database** still contains 5DFL.

## Other years (2000 vs 1998 layout)

2000.5 / 2001 / 2002 files use different KennPar flashes (`0x008079EC`, `0x00807A0A`, `0x00807A2A`) and different `dat_off`. They decode with the same scales, but **axes are not the 1998 live-dump breakpoints** on this truck. Do not subtract those grids cellwise from J90269.06 / J90268.04 and call it a Smarty delta. JSON for every year is under `maps/smarty/udc_stock_vs_factory.json`.

| File | Year | IQ RPM score | FLFL vs A equal? | 5DFL00 vs A nΔ |
|---|---|---|---|---|
| `19990PUAut06J` | 1999 | 1.929 | False | 51 |
| `19990PUAut76J` | 1999 | 1.929 | False | 51 |
| `19990PUMan86J` | 1999 | 1.929 | True | 0 |
| `19990PUMan96J` | 1999 | 1.929 | True | 0 |
| `20000PUAut04J` | 2000 | 1.929 | False | 52 |
| `20000PUAut94J` | 2000 | 1.929 | False | 52 |
| `20000PUMan14J` | 2000 | 1.929 | True | 11 |
| `20000PUMan24J` | 2000 | 1.929 | True | 11 |
| `20005PUAut08J` | 2000.5 | 1.929 | True | 11 |
| `20005PUAut57J` | 2000.5 | 1.929 | True | 11 |
| `20005PUMan16J` | 2000.5 | 1.929 | False | 16 |
| `20005PUMan27J` | 2000.5 | 1.929 | True | 11 |
| `20005PUMan35J` | 2000.5 | 1.929 | False | 16 |
| `20005PUMan46J` | 2000.5 | 1.929 | True | 11 |
| `20010PUAut76J` | 2001 | 1.929 | True | 12 |
| `20010PUAut86J` | 2001 | 1.929 | True | 12 |
| `20010PUMan05J` | 2001 | 1.929 | True | 11 |
| `20010PUMan15J` | 2001 | 1.929 | False | 16 |
| `20010PUMan25J` | 2001 | 1.929 | False | 16 |
| `20010PUMan95J` | 2001 | 1.929 | True | 11 |
| `20020PUAut42J` | 2002 | 1.929 | True | 12 |
| `20020PUAut52J` | 2002 | 1.929 | True | 12 |
| `20020PUMan61J` | 2002 | 1.929 | True | 11 |
| `20020PUMan71J` | 2002 | 1.929 | True | 11 |
| `20020PUMan83J` | 2002 | 1.929 | False | 16 |
| `20020PUMan93J` | 2002 | 1.929 | False | 16 |

## Blockers (SW0–SW9 cell tables)

S03V126 decoded flash (FLASH_KEY) does not contain factory FLFL / 4DTA / 5DFL tables as big-endian KennPar grids (no axis/Z cribs). Five CaTCHER slots are fuel/boost-family F7 streams; L0 is SW0 half-power, not stock. Timing even/odd SW pairs are U2 knobs, not extra SMT copies. No cell-level IQ/timing/5DFL delta vs factory A/B can be produced from the .Smt.

FLASH_KEY search in `S03V126CDR12A.Smt` decoded flash:

- `factory_IQ_rpm_axis_be`: **no hit**
- `factory_4DTA_rpm_axis_be`: **no hit**
- `factory_5DFL_rpm_axis_be`: **no hit**
- `factory_IQ_z_head32_be`: **no hit**
- `factory_4DTA_z_head20_be`: **no hit**
- `factory_5DFL_A_z_head20_be`: **no hit**
- `ascii_FLFLTBZA`: **no hit**
- `ascii_091197`: **no hit**
- `ascii_CUMMINS`: **no hit**

Until a CaTCHER slot is decoded into the same 15×15 / 11×18 / 4×18 physical grids, **per-SW horsepower-style map diffs vs factory cannot be shown**. Marketing HP (+30 / +60 / 65 HP reseller claims) is not a cell table.

## Files written

- `docs/smarty-s03-maps.md` (this page)
- `maps/smarty/*.json` — decoded grids (numbers only)
- `maps/smarty/s03_vs_factory.html` — 1998 UDC stock vs factory A/B

Vendor `.dat` / `.Smt` blobs, VIN/ESN, and write/flash instructions are not in this repository.
