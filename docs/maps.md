# Maps: how tables are stored, and A vs B

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [HTML viewer](../maps/tune_A_vs_B.html) · [Factory A vs B (visual)](../maps/factory-a-vs-b.html) · [Safety](safety.md)

**Open first (decoded numbers in markdown):** [factory-fuel.md](factory-fuel.md) (5DFL A vs B, FLFL, AFC) · [factory-timing.md](factory-timing.md) (4DTA00 / 4DTA01) · [Factory A vs B (visual)](../maps/factory-a-vs-b.html) · [maps/index.md](../maps/index.md).

This page is storage rules, the A-vs-B story in short, and the catalog of all **29** Z-maps. The HTML remains the full viewer.

Decoded artifacts:

- [maps/factory-a-vs-b.html](../maps/factory-a-vs-b.html) — Factory A vs B (visual)
- [maps/tune_A_vs_B.html](../maps/tune_A_vs_B.html) — grids; amber cells differ
- [maps/tune_A_vs_B.json](../maps/tune_A_vs_B.json) — same numbers
- [maps/tune_preview.md](../maps/tune_preview.md) — compact preview (factory pages above are the shop copy)
- [maps/DIFF.md](../maps/DIFF.md) — short blob-level summary

Decode source: Chr0000 meta over the packed ReadByNTN dumps. **29** Z-maps, **2172** scalars. Passwords and boot-copy ITNs are not in the dumps.

## Storage on the wire / in the dump

KennPar axes and tables are **not** “17×4 because a comment said so.” Live layout:

1. **Axis (`X` / `Y`)**  
   First two bytes are **`u16` big-endian = byte count of the point list**, not the number of points.  
   If each point is a `u16` (size 2), point count is `nbytes / 2`. Points start at offset 2. Physical value is `raw * scale + add` from the catalog meta.

2. **Z table**  
   Z is **Y rows × X columns** (row-major, Y varies slower). Cell size is usually 2 bytes, big-endian, then the same scale/add.  
   Needed length is `ny * nx * cell_size`. If the dumped Z blob is shorter than that, the decode pads with empty cells and records a truncation note.

3. **Catalog comments lie about shape.**  
   Example: 5D fuel comments talk about 17×4. The axis prefixes on these boxes are **4 × 18** (Y × X). Prefer the prefix over the comment.

The decoder in [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) (`python/decode_tune.py`) implements that rule. If `nbytes` is missing or not divisible by the element size, it falls back to a short raw walk; that fallback is a safety net, not the normal Dodge path.

## The calibration difference that matters

Same ECM P/N and ROM date. Timing conversion and timing grids match. **Fuel does not.**

| Map | ITN | Dims (Y × X) | Units | A vs B |
|---|---|---|---|---|
| `4DTA00ZA` transient timing | `1041` | 11 × 18 | DEG | **same** |
| `4DTA01ZA` steady-state timing | `103E` | 11 × 18 | DEG | **same** |
| `5DFL00ZA` transient fuel | `1059` | 4 × 18 | MM3S | **differs** |
| `5DFL01ZA` steady-state fuel | `1056` | 4 × 18 | MM3S | **differs** |
| `FLFLTBZA` mg/stroke conversion | `8014` | 15 × 15 | MG/S | **same** |

`4DTA00ZA` raw blob is 512 bytes. The 11×18 table is 396 data bytes plus axis overhead elsewhere. The first raw-byte difference between A and B is at **byte 480**, past the decoded table. Treat the **decoded grid** as matching.

`5DFL00ZA` / `5DFL01ZA` first raw-byte difference is at **byte 114**, inside the 4×18 table. That is a real cal delta.

On the 100% (full throttle) row, A is generally **richer** than B in the mid/high RPM columns. Full A and B grids plus A−B: [factory-fuel.md](factory-fuel.md). Snapshot:

- 1200 RPM: 88.315 / 85.53
- 2000 RPM: 98.506 / 95.788
- 2600 RPM: 106.998 / 102.989
- 2800 RPM: 108.968 / 97.011
- 3000 RPM: 109.987 / 90.014

Steady-state `5DFL01ZA` shows the same pattern. Low-load rows (0 / 25 / 50) match or nearly match. The silk-screen codes are not “the same tune with a sticker change.”

Altitude derate `ATFLLMZA` (4×18) **matches**. Boost-based AFC limiter `AFFLLMZA` is a separate story below.

## AFFLLMZA (AFC limiter) — differs, dump truncated

`AFFLLMZA` (ITN `104F`) is the AFC look-up: fueling limit vs boost × RPM. Axes decoded to **14 × 21**. The Z ITN was only **512 of 588 bytes** (256 of 294 cells). I6Pull requested the catalog size (512).

**RPM and boost breakpoints are not the same on A and B** (A has 700 RPM and 25/30 inHg; B has 4500 RPM and 100/110 inHg instead). The HTML viewer is **index-aligned**, so column 2 of A is not the same RPM as column 2 of B. Same-breakpoint slices (A richer at low boost; B’s 0 inHg row falls to ~45 mm³/s from 1280 RPM) are in [factory-fuel.md](factory-fuel.md).

Count this as a **third decoded-table difference**, but an **incomplete** one. Do not treat the 14×21 grid as fully known. Re-pulling a longer Z is a tool change; this repo does not include a write path and does not instruct one. The HTML “maps that differ” summary highlighted 5D fuel because those two tables are complete 4×18 dumps. The JSON `equal` flag is false for `AFFLLMZA` as well.

## Every decoded Z-map (29)

Dims are **Y × X** from the axis prefixes. `NAK 0D 08 48` means the ECM negatively acknowledged the ReadByNTN (`0x48`) for that ITN or its axis. Those maps are in the Chr0000 list but **not implemented / not readable on this Dodge cal**.

| Name | ITN | Units | Y × X | A vs B | Notes |
|---|---|---|---|---|---|
| `4DTA00ZA` | 1041 | DEG | 11 × 18 | same | Transient timing. Axes `4DTA00YA` (MM3S) × `4DTA00XA` (RPM). |
| `4DTA01ZA` | 103E | DEG | 11 × 18 | same | Steady-state timing. |
| `5DFL00ZA` | 1059 | MM3S | 4 × 18 | **differs** | Transient fuel for 4D fueling. **Main complete cal delta.** |
| `5DFL01ZA` | 1056 | MM3S | 4 × 18 | **differs** | Steady-state fuel. **Main complete cal delta.** |
| `AABSPRZA` | 8246 | INHG | — | n/a | X, Y, and Z NAK. |
| `AFFLLMZA` | 104F | MM3S | 14 × 21 | **differs (truncated)** | AFC boost limiter. Z 512/588 bytes. |
| `ATFLLMZA` | 10A3 | MM3S | 4 × 18 | same | Altitude derate fuel limit. |
| `BSTATBZA` | 8191 | DEG | 6 × 6 | same | Minimum advance for misfire. |
| `CAICTAZA` | 1038 | DEG | — | n/a | Y NAK; empty axes. Coolant advance. |
| `CBDCAT` | 803F | NONE | 2 × 2 | same | Cylinder balancing component-3. |
| `CBDSCT` | 8042 | NONE | 2 × 2 | same | Cylinder balancing stop compensation. |
| `CKEXFLZA` | 825E | MM3S | — | n/a | X/Y/Z NAK. Crank exit fuel. |
| `CKIIFLZA` | 8261 | MM3S | — | n/a | X/Y/Z NAK. Crank initial fuel. |
| `CPCS02YA` | 11D2 | NONE | 3 × 13 | same | Polytropic / compression-ratio related axis table. |
| `CPDSZA` | 108A | PSIA | 7 × 13 | same | Desired cylinder pressure. |
| `FLCDICZA` | 81F0 | MM3S | 5 × 9 | same | Cold-temp incremental fuel. |
| `FLFLTBZA` | 8014 | MG/S | 15 × 15 | same | Fuel units → mg/stroke. UDC/KennPar name overlap. |
| `FLTATBZA` | 8017 | DEG | 12 × 12 | same | Line-delay timing offset. |
| `HG00ZA` | 13F6 | MM3S | — | n/a | X/Y/Z NAK. Hybrid governor transient fuel. |
| `HG01ZA` | 13F3 | MM3S | — | n/a | X/Y/Z NAK. Hybrid governor SS fuel. |
| `IHHITDTB` | 81C9 | FDEG | — | n/a | Y NAK. High-speed intake-heater thresholds. |
| `IHLOTDTB` | 81D3 | FDEG | — | n/a | Y NAK. Low-speed intake-heater thresholds. |
| `IHPHTMZA` | 81B2 | SEC | 4 × 7 | same | Intake-air heater postheat time. |
| `IHPHTZ1A` | 8259 | SEC | — | n/a | X/Y/Z NAK. Postheat Z1. |
| `IHPRTMZA` | 825A | SEC | 12 × 12 listed | n/a | Z NAK. Preheat time. |
| `MTTQMPZA` | 1460 | FTLB | — | n/a | X/Y/Z NAK. Max torque table. |
| `TCSTESZA` | 82C2 | RPM | — | n/a | X/Y/Z NAK. Stall-torque engine-speed limit. |
| `WSTATB` | 1076 | DEG | — | n/a | Y NAK. Wet-stack timing vs IMT / ambient. |
| `WSTAZA` | 82D4 | DEG | — | n/a | X/Y/Z NAK. Wet-stack timing (RPM/fuel thresholds). |

Decode notes in the HTML also record **260 NAK scalars**, **11 missing**, 0 short/unreadable, for the scalar pass. NAKs on this Dodge cal are expected. Do not treat 29 as “every Cummins ISB map.”

## RPM axes (fuel and timing)

Timing X (`4DTA00XA` / `4DTA01XA`):  
700, 800, 1000, 1200, 1280, 1400, 1580, 1800, 2000, 2200, 2400, 2500, 2600, 2700, 2800, 3000, 3250, 3800.

Fuel X (`5DFL00XA` / `5DFL01XA`):  
600, 800, 1000, 1200, 1280, 1400, 1580, 1800, 2000, 2200, 2400, 2500, 2600, 2700, 2800, 3000, 3250, 3800.

Fuel Y is 0, 25, 50, 100 (percent-ish MM3S-scaled load). Timing Y is a fuel/load axis in MM3S, not identical breakpoints to 5D.

`FLFLTBZA` X (`FLFLESXA`) is RPM 200…3500 (15 pts). Y (`FLFLFLYA`) is a fuel-unit axis 0…240.

## Scalars

The JSON includes 2172 decoded scalars. On the order of **103** differ. Many are runtime (hours, key-on, VSS, faults). Cal-ish ITNs that differ in the raw capture include `0003` CAL_DATE, `0006` DAT_PLAT, `001D` DATADATE, `801D` FLCKSPTM, plus the fuel Z blobs above. A long tail of diagnostic/config ITNs also differ; see [maps/DIFF.md](../maps/DIFF.md). Do not retune from a scalar list without reading the comment and units in the HTML.

## What this is not

These grids are **engineering units after scale/add**, from a live upload. They are not a Smarty slot, not a Quadzilla AID curve, and not a flash patch. Editing the JSON and sending it back to the ECM is not documented here and is not supported by I6Pull.
