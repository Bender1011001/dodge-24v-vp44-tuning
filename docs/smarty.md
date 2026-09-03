# Smarty / UDC (VP44) — what is known here

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

Live factory tables (same KennPar names): [factory-fuel.md](factory-fuel.md), [factory-timing.md](factory-timing.md).

**Decoded UDC stock vs this truck’s factory maps:** [smarty-s03-maps.md](smarty-s03-maps.md) (1998.5–99 `FLFL` / `4DTA` / `5DFL` cell tables). Browser view: [maps/smarty/s03_vs_factory.html](../maps/smarty/s03_vs_factory.html).

Smarty S03 (MADS / TomElectronics) is a **handheld** VP44 tuner ecosystem with a PC application **UDC Pro RT**. It is a different product from Quadzilla Adrenaline. Do not mix ARM7 32 KB Adrenaline facts into S03 work.

This master repo **does not** ship UDC Pro, year `.dat` stock databases, `.Smt` firmware, or recovered keys. Those are vendor IP. Private lab analysis scripts named `analyze_s03_*.py` are **not** copied here, and they are **not** in the public [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) tree (that repo is Adrenaline-focused).

## Why Smarty shows up on a CM551 truck

UDC’s calibration vocabulary uses the same **KennPar names** as the Dodge E2M / this dump: `FLFLTBZA`, `FLFLESXA`, `4DTA00ZA`, `4DTA00XA`, and related fuel/timing identifiers. A tuner who has used UDC already knows those strings. The live CM551 upload in `maps/` is an independent, owner-captured source for the **same names** on two physical boxes.

That overlap is why a known-plaintext attack (KPA) against encrypted UDC year `.dat` files was attempted in the lab: locate `FLFLTBZA` / `4DTA00ZA` windows in a ciphertext `19980PUMan44J.dat`-class file and compare them to a **plaintext CM551 flash layout**.

## KPA is frozen

XOR-key guessing on the year `.dat` files is **frozen**. The lab harness (`analyze_s03_datkpa.py`) is written **not** to brute period-N keys. It waits for a plaintext CM551 **image** (Calterm upload, licensed INCAL, or BDM) and then tests structured transforms against already-located 1998 windows, for example:

| KennPar | Role in that harness (ciphertext offsets are lab-local) |
|---|---|
| `FLFLTBZA` | mg/stroke table |
| `FLFLESXA` | RPM axis |
| `FLFLFLYA` | fuel-unit axis |
| `4DTA00ZA` | timing table |
| `4DTA00XA` | RPM axis |

The KennPar dumps in this repository are **not** that flash image. They are ITN payloads without flash addresses. They do **not** unfreeze XOR-key guessing.

Year `.dat` **cell tables** on this page come from plaintext already produced by the recovered UDC native decoder (`LIB_0203` `PCGet`) in the private lab — **not** from a new KPA run. Vendor `.dat` / `.Smt` blobs stay out of this git tree. **Do not brute XOR keys. Do not unpack Themida.** This page will not describe those attacks.

## What is known without redistributing vendor files

- UDC Pro RT is a Windows .NET application plus native DLLs. Stock `db/*.dat` files and user-saved DocSeri documents are **different** containers. Details stay in the private lab writeup; they are not required to read the CM551 maps.
- Handheld `.Smt` / SmartyUSB update path is also a separate problem from CM551 ReadByNTN. Lab notes say the USB loader ships header records plus flash chunks; recovering the handheld MCU image was **not** finished from that path alone.
- `S03V126CDR12A.Smt` in the lab is Smarty S03, **not** the Quadzilla ARM7 image.

None of that is needed to compare J90269.06 vs J90268.04. Use [factory-fuel.md](factory-fuel.md) and [factory-timing.md](factory-timing.md).

## What remains unknown (stated as unknown)

- **SW0–SW9 as KennPar grids.** Handheld CaTCHER slots are F7 streams, not `FLFL`/`4DTA`/`5DFL` tables. There is still no cell-level delta for advertised power levels vs factory A/B. See [smarty-s03-maps.md](smarty-s03-maps.md).
- Whether UDC’s later-year families (2000+) correspond 1:1 to silk-screen `J90268.04` vs `J90269.06`. Filenames encode year/transmission/family, not an ECM code. 1998 UDC **manual** WOT `5DFL00` is close to factory **B**, not A.
- Handheld U2 / AT89 firmware as a readable image in this project.

## Pointers

- **Smarty S03 vs factory maps:** [smarty-s03-maps.md](smarty-s03-maps.md)
- KennPar names and live tables: [factory-fuel.md](factory-fuel.md), [factory-timing.md](factory-timing.md), `maps/`.
- Read-only puller: [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull).
- Adrenaline (not Smarty): [quadzilla.md](quadzilla.md) and [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed).
- `analyze_s03_*.py`: local `quadzilla_rev` only. Not published here on purpose.
