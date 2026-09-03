# Inventory: this repo vs companions

## In this master repository

| Path | What |
|---|---|
| [README.md](../README.md) | Index, companion links, safety box |
| [LICENSE](../LICENSE) | CC BY 4.0 for docs and dumps; companion license note at end |
| [docs/truck.md](truck.md) | Vehicle / VP44 / 3-pin datalink |
| [docs/cm551.md](cm551.md) | Two boxes, identity, dump vs flash |
| [docs/maps.md](maps.md) | Table format, all 29 Z-maps, 5D fuel |
| [docs/protocol.md](protocol.md) | ReadByNTN `0x48`/`0x49`, INLINE quirks |
| [docs/quadzilla.md](quadzilla.md) | Adrenaline summary + pointer |
| [docs/smarty.md](smarty.md) | UDC/KennPar overlap, KPA frozen |
| [docs/safety.md](safety.md) | Read-only rules |
| [maps/tune_A_vs_B.html](../maps/tune_A_vs_B.html) | Decoded compare (browser) |
| [maps/tune_A_vs_B.json](../maps/tune_A_vs_B.json) | Decoded compare (machine) |
| [maps/tune_preview.md](../maps/tune_preview.md) | Featured tables in markdown |
| [maps/DIFF.md](../maps/DIFF.md) | Blob-level A vs B notes |
| [maps/A_identity.json](../maps/A_identity.json), [B_identity.json](../maps/B_identity.json) | Identity, no VIN/ESN |
| [maps/A_dump.json](../maps/A_dump.json), [B_dump.json](../maps/B_dump.json) | Packed ITNs; `81AC` redacted |

## Companion GitHub repos (do not duplicate here)

| Repo | Owns |
|---|---|
| [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) | C# puller, `SAFETY.md`, `docs/protocol.md`, `catalog/`, `python/decode_tune.py` (MIT) |
| [cm551-dodge-dumps](https://github.com/Bender1011001/cm551-dodge-dumps) | Canonical dump publication (`A/`, `B/`, `decoded/`). Files under `maps/` here are copies of the redacted dumps plus decode outputs. |
| [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) | Adrenaline decompilation notes, AID profiles, x2com C. No CM551 dumps. |

## Local lab (not this git tree)

`E:\code.projects\quadzilla_rev` is the working lab: INLINE experiments, Smarty `analyze_s03_*.py`, captures, Ghidra/IDA databases. It is **not** mirrored here.

`E:\code.projects\cm551-i6pull` and `E:\code.projects\cm551-dodge-dumps` are the local clones of the two CM551 GitHub repos.

## Deliberately absent

- Calterm installers and `Chr0000.e2m` / `Chr9900.e2m`
- INSITE, `CureCore.dll`, Ghidra projects of Cummins DLLs
- Password ITNs, VIN, ESN
- UDC Pro / Smarty commercial `.dat` / `.Smt` blobs
- Entire `captures/`, `official_s03/`, I6Pull `_scan_*` experiment scripts
- Any write-to-ECM tool or exploit/PoC

If you need the puller, clone i6pull. If you need only dumps, clone dodge-dumps or use `maps/` here. If you need Adrenaline firmware RE, use the Quadzilla repo. This repository is the **index and the truck writeup**.
