# Inventory: this repo vs companions

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

## In this master repository

| Path | What |
|---|---|
| [README.md](../README.md) | Shop landing: two cals, fuel/timing links, safety, companions |
| [LICENSE](../LICENSE) | CC BY 4.0 for docs and dumps; companion license note at end |
| [docs/factory-fuel.md](factory-fuel.md) | Decoded 5DFL A vs B, FLFL, AFC, altitude |
| [docs/factory-timing.md](factory-timing.md) | Decoded 4DTA00 / 4DTA01 |
| [docs/quadzilla-vs-factory.md](quadzilla-vs-factory.md) | Adrenaline overlay vs those KennPars |
| [docs/truck.md](truck.md) | Vehicle / VP44 / 3-pin datalink |
| [docs/cm551.md](cm551.md) | Two boxes, identity, dump vs flash |
| [docs/maps.md](maps.md) | Table format, all 29 Z-maps |
| [docs/protocol.md](protocol.md) | ReadByNTN `0x48`/`0x49`, INLINE quirks |
| [docs/quadzilla.md](quadzilla.md) | Adrenaline RE summary + pointer |
| [docs/smarty.md](smarty.md) | UDC/KennPar overlap, KPA frozen, pointer to decoded S03 maps |
| [docs/smarty-s03-maps.md](smarty-s03-maps.md) | 1998 UDC stock FLFL / 4DTA / 5DFL vs factory A/B; SW0–9 blocker |
| [docs/safety.md](safety.md) | Read-only rules |
| [maps/index.md](../maps/index.md) | Map-file index |
| [maps/tune_A_vs_B.html](../maps/tune_A_vs_B.html) | Decoded compare (browser) |
| [maps/tune_A_vs_B.json](../maps/tune_A_vs_B.json) | Decoded compare (machine) |
| [maps/tune_preview.md](../maps/tune_preview.md) | Featured tables in markdown |
| [maps/DIFF.md](../maps/DIFF.md) | Blob-level A vs B notes |
| [maps/A_identity.json](../maps/A_identity.json), [B_identity.json](../maps/B_identity.json) | Identity, no VIN/ESN |
| [maps/A_dump.json](../maps/A_dump.json), [B_dump.json](../maps/B_dump.json) | Packed ITNs; `81AC` redacted |
| [maps/smarty/](../maps/smarty/) | Decoded 1998 UDC grids (JSON) + `s03_vs_factory.html`; numbers only, no vendor blobs |

## Companion GitHub repos (do not duplicate here)

| Repo | Owns |
|---|---|
| [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) | C# puller, `SAFETY.md`, `docs/protocol.md`, `catalog/`, `python/decode_tune.py` (MIT) |
| [cm551-dodge-dumps](https://github.com/Bender1011001/cm551-dodge-dumps) | Canonical dump publication (`A/`, `B/`, `decoded/`). Files under `maps/` here are copies of the redacted dumps plus decode outputs. |
| [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) | Adrenaline decompilation notes, AID profiles, x2com C. No CM551 dumps. |

## Local lab (not this git tree)

A private working tree holds INLINE experiments, Smarty analysis scripts, captures, and IDA/Ghidra databases. It is **not** mirrored here. Public CM551 clones are [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) and [cm551-dodge-dumps](https://github.com/Bender1011001/cm551-dodge-dumps).

## Deliberately absent

- Calterm installers and `Chr0000.e2m` / `Chr9900.e2m`
- INSITE, `CureCore.dll`, Ghidra projects of Cummins DLLs
- Password ITNs, VIN, ESN
- UDC Pro / Smarty commercial `.dat` / `.Smt` blobs
- Entire `captures/`, `official_s03/`, I6Pull `_scan_*` experiment scripts
- Any write-to-ECM tool or exploit/PoC

If you need the puller, clone i6pull. If you need only dumps, clone dodge-dumps or use `maps/` here. If you need Adrenaline firmware RE, use the Quadzilla repo. This repository is the **index, the factory fuel/timing tables, the truck writeup, and decoded UDC stock vs factory tables**.
