# Smarty / UDC (VP44) — what is known here

Smarty S03 (MADS / TomElectronics) is a **handheld** VP44 tuner ecosystem with a PC application **UDC Pro RT**. It is a different product from Quadzilla Adrenaline. Do not mix ARM7 32 KB Adrenaline facts into S03 work.

This master repo **does not** ship UDC Pro, year `.dat` stock databases, `.Smt` firmware, or recovered keys. Those are vendor IP. The local lab (`E:\code.projects\quadzilla_rev`) has analysis scripts named `analyze_s03_*.py`. They are **not** copied here, and they are **not** in the public [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) tree (that repo is Adrenaline-focused).

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

The KennPar dumps in this repository are **not** that flash image. They are ITN payloads without flash addresses. They do **not** unfreeze the KPA by themselves.

Status recorded in lab notes: year `.dat` plaintext still needs a CM551 KPA pair or work inside the packed UDC runtime. **Do not brute XOR keys. Do not unpack Themida.** This page will not describe those attacks.

Until a legitimate plaintext image exists, treat UDC stock `.dat` as opaque vendor data.

## What is known without redistributing vendor files

- UDC Pro RT is a Windows .NET application plus native DLLs. Stock `db/*.dat` files and user-saved DocSeri documents are **different** containers. Details stay in the private lab writeup; they are not required to read the CM551 maps.
- Handheld `.Smt` / SmartyUSB update path is also a separate problem from CM551 ReadByNTN. Lab notes say the USB loader ships header records plus flash chunks; recovering the handheld MCU image was **not** finished from that path alone.
- `S03V126CDR12A.Smt` in the lab is Smarty S03, **not** the Quadzilla ARM7 image.

None of that is needed to compare J90269.06 vs J90268.04. Use [maps.md](maps.md).

## What remains unknown (stated as unknown)

- A public, legal mapping from UDC slot / “HP” labels to the 5D fuel cells in `maps/tune_A_vs_B.html`.
- Plaintext of the shipped year `.dat` database.
- Whether UDC’s 1998 vs 2000 families correspond 1:1 to silk-screen `J90268.04` vs `J90269.06`. The live dumps show those two codes differ in 5D fuel (and in the truncated AFC limiter). UDC filenames encode year/transmission/family; that is not the same identifier as an ECM code.
- Handheld U2 / AT89 firmware as a readable image in this project.

## Pointers

- KennPar names and live tables: this repo, `maps/` and [maps.md](maps.md).
- Read-only puller: [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull).
- Adrenaline (not Smarty): [quadzilla.md](quadzilla.md) and [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed).
- `analyze_s03_*.py`: local `quadzilla_rev` only. Not published here on purpose.
