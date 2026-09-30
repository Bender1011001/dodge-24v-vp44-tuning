# Smarty / UDC (VP44) — what is known here

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

Live factory tables (same KennPar names): [factory-fuel.md](factory-fuel.md), [factory-timing.md](factory-timing.md).

**Decoded UDC stock vs this truck’s factory maps:** [smarty-s03-maps.md](smarty-s03-maps.md) (1998.5–99 `FLFL` / `4DTA` / `5DFL` cell tables). Browser view: [maps/smarty/s03_vs_factory.html](../maps/smarty/s03_vs_factory.html).

Smarty S03 (MADS / TomElectronics) is a **handheld** VP44 tuner ecosystem with a PC application **UDC Pro RT**. It is a different product from Quadzilla Adrenaline. Do not mix ARM7 32 KB Adrenaline facts into S03 work.

This master repo **does not** ship UDC Pro, year `.dat` stock databases, `.Smt` firmware, or any key material. Those are vendor IP. The S03 analysis scripts are not published here or in [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) (that repo is Adrenaline-focused).

## Why Smarty shows up on a CM551 truck

UDC’s calibration vocabulary uses the same **KennPar names** as the Dodge E2M / this dump: `FLFLTBZA`, `FLFLESXA`, `4DTA00ZA`, `4DTA00XA`, and related fuel/timing identifiers. A tuner who has used UDC already knows those strings. The live CM551 upload in `maps/` is an independent, owner-captured source for the **same names** on two physical boxes.

## How the UDC stock tables on this page were obtained

The year cell tables come from the vendor's own decoder library (`LIB_0203`, `PCGet`) run on the vendor's own stock files, not from breaking the year-file
encryption. An earlier attempt to locate known plaintext (`FLFLTBZA` / `4DTA00ZA` windows) in the encrypted year files was abandoned without a result and is not
described or published here. The vendor `.dat` and `.Smt` files stay out of this git tree.

The KennPar dumps in this repository are ITN payloads without flash addresses. They are not a flash image and cannot be used to locate or test anything inside a vendor container.

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
