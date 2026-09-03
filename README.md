# Dodge 24-valve 5.9 VP44 — factory maps

A Dodge Ram with a 24-valve **5.9 Cummins** (ISB), Bosch **VP44** injection pump, and Cummins **CM551** engine controller. Common model years **1998.5–2002**.

This repository is the owner-captured **factory calibration** from two physical CM551 modules, decoded to engineering units. It is for reading what the boxes already contain. It is not a flash kit, not a programmer, and not a substitute for Cummins or Chrysler service tools.

## Open first

| Need | Page |
|---|---|
| Fuel (5DFL A vs B, conversion, AFC) | **[docs/factory-fuel.md](docs/factory-fuel.md)** |
| Timing (4DTA00 vs 4DTA01) | **[docs/factory-timing.md](docs/factory-timing.md)** |
| Adrenaline overlay vs those KennPars | **[docs/quadzilla-vs-factory.md](docs/quadzilla-vs-factory.md)** |
| Smarty S03 vs factory maps | **[docs/smarty-s03-maps.md](docs/smarty-s03-maps.md)** |
| All 29 maps in a browser | **[maps/tune_A_vs_B.html](maps/tune_A_vs_B.html)** |

Index of map files: [maps/index.md](maps/index.md). How tables are stored, and the other 24 maps: [docs/maps.md](docs/maps.md).

## Two factory calibrations

Same ECM part number and ROM date. Different silk-screen codes. **Timing tables match. Fuel tables do not.**

| | ECM A | ECM B |
|---|---|---|
| ECM code | J90269.06 | J90268.04 |
| Plate | 6BTA 5.9 Li, FP98455, Chrysler T-300 | ISB 235, 98453, Chrysler automotive |
| P/N | 03942336 | 03942336 |
| ROM date | 091197 | 091197 |
| Cal date | 062800 | 102198 |

On the 100% (full throttle) row of `5DFL00ZA` / `5DFL01ZA`, **A is richer** than B from about 1200 RPM up, with the largest gap at **2800–3000 RPM** (A stays near 107–110 mm³/s; B drops into the 87–97 range). Part-load 5DFL rows match. Boost AFC (`AFFLLMZA`) also differs, but that dump is truncated and the axes are not the same — details on the fuel page.

## Safety

**Read-only.** These notes describe KennPar ITNs that were *uploaded* from hardware the owner already had. They do not describe how to program, erase, or bootloader an ECM.

- Do **not** treat files in `maps/` as a flash image or a download-to-ECM file.
- Do **not** use this writeup as a running-engine fueling interface.
- Full rules: [docs/safety.md](docs/safety.md).

## Adrenaline and Smarty

[Quadzilla Adrenaline](docs/quadzilla-vs-factory.md) is a **piggyback** on the ECM↔pump path. It does not contain these CM551 tables and does not rewrite them. Firmware reverse-engineering lives in a companion repo (below). This master repo only explains how Adrenaline *adjustments relate* to factory `5DFL` / `4DTA` / `FLFL` / AFC — and where that mapping is still unknown.

[Smarty / UDC](docs/smarty.md) uses the same KennPar *names*. Decoded **1998 UDC stock** tables versus factory A/B: **[Smarty S03 vs factory maps](docs/smarty-s03-maps.md)**. Stock UDC `.dat` databases and handheld `.Smt` firmware are not published here. Handheld SW0–9 are **not** those year-stock files.

## Companion repositories

This master repo **links** the published pieces. It does not duplicate their binaries or tool trees.

| Repo | What it is |
|---|---|
| [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) | Read-only INLINE 6 puller (MIT). How the KennPar read was done. |
| [cm551-dodge-dumps](https://github.com/Bender1011001/cm551-dodge-dumps) | Canonical packed dumps + decoded HTML (CC BY 4.0). Vehicle id redacted. |
| [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) | Adrenaline (DADR9802) firmware / AID / x2com research. |

## Other documentation

1. [docs/truck.md](docs/truck.md) — vehicle, ECM, VP44, 3-pin datalink vs J1708.
2. [docs/cm551.md](docs/cm551.md) — the two boxes, identity fields, KennPar dump vs flash image.
3. [docs/maps.md](docs/maps.md) — table storage, every decoded Z-map.
4. [docs/protocol.md](docs/protocol.md) — ReadByNTN `0x48` / `0x49`, CAN, INLINE 6 quirks.
5. [docs/quadzilla.md](docs/quadzilla.md) — Adrenaline RE facts (verified vs unknown).
6. [docs/inventory.md](docs/inventory.md) — what lives here vs the companions.

## License

Documentation and the redacted dumps here are [CC BY 4.0](LICENSE). The INLINE 6 tool is MIT in its own repo. Quadzilla research keeps the license of [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed).
