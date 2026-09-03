# Dodge 24-valve 5.9 ISB VP44 — master notes

This is the index for one owner-captured Dodge Ram with a 24-valve 5.9 Cummins, a Bosch **VP44** injection pump, and a Cummins **CM551** engine controller (roughly model years **1998.5–2002**).

The writeup is for people who want to **understand the calibration that is already on the boxes** and how it was read. It is not a flash kit, not a programming guide, and not a substitute for Cummins or Chrysler service tools.

Two physical CM551 modules were dumped **read-only** over the Dodge 3-pin Cummins datalink with a Cummins INLINE 6:

| | ECM A | ECM B |
|---|---|---|
| ECM code | J90269.06 | J90268.04 |
| Plate | 6BTA 5.9 Li, FP98455, Chrysler T-300 | ISB 235, 98453, Chrysler automotive |
| P/N | 03942336 | 03942336 |
| ROM date | 091197 | 091197 |
| Cal date | 062800 | 102198 |
| Engine hours | 13130:48:02 | 10196:32:59 |
| ECM VSS miles | ~81 | ~287919 |
| ITNs pulled | 667 / 667 | 667 / 667 |

The same hardware family (P/N `03942336`, ROM `091197`) carries two different printed calibration codes. Transient and steady-state **4D timing** tables match. The **5D fuel** tables do not. That is the useful cal difference.

## Safety (read this first)

**Read-only.** These notes describe how KennPar ITNs were *uploaded* from hardware the owner already had. They do not describe how to program, erase, or bootloader an ECM.

- Do **not** treat files in `maps/` as a flash image or a download-to-ECM file.
- Do **not** transmit 11-bit VP44 IDs `0x112`, `0x512`, `0x001`, or `0x500`.
- Do **not** request password ITNs or BOOTDST / boot-copy ITNs.
- Full rules: [docs/safety.md](docs/safety.md).

## Companion repositories

This master repo **links** the three published pieces of work. It does not duplicate their binaries or tool trees.

| Repo | What it is |
|---|---|
| [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) | Read-only INLINE 6 puller (MIT). Build and protocol for the KennPar read. |
| [cm551-dodge-dumps](https://github.com/Bender1011001/cm551-dodge-dumps) | Canonical packed dumps + decoded HTML (CC BY 4.0). VIN redacted. |
| [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) | Quadzilla Adrenaline (DADR9802) firmware / AID / x2com research. |

Local lab (not published as a whole): `E:\code.projects\quadzilla_rev`. Smarty/UDC scripts live there; they are **not** copied here.

## Documentation

1. [docs/truck.md](docs/truck.md) — vehicle, ECM, VP44, 3-pin datalink vs J1708, why INSITE said J1939.
2. [docs/cm551.md](docs/cm551.md) — the two boxes, identity fields, hours, KennPar dump vs flash image.
3. [docs/maps.md](docs/maps.md) — table storage, every decoded Z-map, A vs B, 5D fuel.
4. [docs/protocol.md](docs/protocol.md) — ReadByNTN `0x48` / `0x49`, CAN IDs, J1939 TP, INLINE 6 quirks.
5. [docs/quadzilla.md](docs/quadzilla.md) — Adrenaline on this truck; what is verified vs still unknown.
6. [docs/smarty.md](docs/smarty.md) — Smarty / UDC VP44 `.dat` work; KPA frozen; KennPar name overlap.
7. [docs/safety.md](docs/safety.md) — read-only rules.
8. [docs/inventory.md](docs/inventory.md) — what lives here vs the companion repos.

## Maps in this repo (offline)

Open [maps/tune_A_vs_B.html](maps/tune_A_vs_B.html) in a browser. Yellow cells differ.

| File | Contents |
|---|---|
| [maps/tune_A_vs_B.html](maps/tune_A_vs_B.html) | Decoded maps and scalars, A vs B |
| [maps/tune_A_vs_B.json](maps/tune_A_vs_B.json) | Same decode as JSON |
| [maps/tune_preview.md](maps/tune_preview.md) | Timing, 5D fuel, FLFLTBZA preview tables |
| [maps/DIFF.md](maps/DIFF.md) | Short cal vs runtime summary |
| [maps/A_identity.json](maps/A_identity.json) / [B_identity.json](maps/B_identity.json) | Identity without VIN/ESN |
| [maps/A_dump.json](maps/A_dump.json) / [B_dump.json](maps/B_dump.json) | Packed ITN dumps; VIN at ITN `81AC` redacted |

## License

Documentation and the redacted dumps here are [CC BY 4.0](LICENSE). The INLINE 6 tool is MIT in its own repo. Quadzilla research keeps the license of [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed).
