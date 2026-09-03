# Quadzilla Adrenaline on this truck

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

Tuner-facing overlay vs factory `5DFL` / `4DTA` / AFC: **[quadzilla-vs-factory.md](quadzilla-vs-factory.md)**. This page is the RE fact list (verified vs unknown).

Quadzilla **Adrenaline** (DADR9802 class) is an inline diesel tuner sold for **1998–2002 Dodge Ram 24-valve Cummins / VP44**. It sits in the ECM↔pump path and exposes tuner parameters (AIDs) over USB CDC and BLE (iQuad / x2com). It is a **separate computer** from the CM551. CM551 KennPar dumps in this master repo are not Adrenaline firmware, and Adrenaline AIDs are not KennPar ITNs.

Detailed artifacts live in [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed). This page is a factual summary for the same truck family. It does **not** copy firmware images, the PC updater, the APK, or Ghidra projects.

Prefer the audited notes in [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) over older narrative writeups. Tuner overlay vs these factory maps: [quadzilla-vs-factory.md](quadzilla-vs-factory.md).

## What is verified (static / file)

Re-audit date on the lab map: **2026-08-22**.

- **`.qz` packaging:** ciphertext-feedback XOR over **uncompressed** Intel HEX (`:10400000…`, 2000 `:10` records, CRLF, no EOF). Not zlib/deflate. Not the Smarty `.Smt` XOR.
- **Image:** ARM7TDMI, **32,000 bytes**, file offset 0 maps to abs `0x4000` (`0x4000`–`0xBCFF`). Round-trip decrypt stock `.qz` → bin → encrypt → decrypt matches `firmware_v2.8.4HF.bin` (sha256 prefix `1ae519ba6194e8f7…` in the lab notes).
- **Toolkit name that exists in the lab tree:** `quadzilla_toolkit.py`. `firmware_crypto.py` / `quadzilla_tool.py` are **not** current names in that tree.
- **AID Table 1** (`sub_7C1C`) starts at `0xA91C` with firmware segment cuts. AID **113–136** are SRAM `0x200B3B`–`0x200B69` (2-byte stride), matching Dodge 1998–2002 JSON **boost-curve** names.
- **AID Table 2** (`sub_7C68`) starts at `0xAD18` (not `0xAE80`); stop before code at `0xB114`. Table 2 words are **RAM pointers**, not 1–4 size integers. Width comes from `sub_7BF8` / `x2com_get_data_size`.
- **AID size brackets** (CRC and x2com): `<75` → 1 byte, `<150` → 2, `<185` → 3, `<220` → 4. CRC-8 init `0xFF`, poly `0x1D`, final bitwise NOT.
- **Profiles:** union of unique AIDs across 14 fetched iQuad catalog JSONs = **117**. Local Dodge 2.7 JSON has **73**. APK `vehicle_profiles.json` Demonstration profile has **32**. Do not treat 117 as one vehicle profile.
- **DTCs:** APK SQLite `dtc` = 1,162 rows (1,155 distinct `field1`, plus one empty code). CSV/JSON/website export = 1,258 rows / 1,254 distinct. JSON adds P-codes not in the APK DB. Do not smash the SQLite to match the export. DTC **text is not in the 32 KB image**.
- **MCU fueling chain (ASM, structural — not a live VP44 bench proof):** hardware pulse consumer is AT91 **TC0_RC** (`sub_6FA0` store to `0xFFFA001C`). Applied stretch comes from `sub_4A94` (AID **85** working copy at `0x200590`) minus AID **13** backdown, then `*24+3`. SRAM `0x200604` is a **telemetry/status** word (AID 149 scaled copy), **not** the TC0 operand.

Closed structural chain:

**AID 85 → `0x200B30` / `0x200590` → `sub_601C` clamp → `sub_4A94` → AID 13 subtract → `sub_6FA0` TC0_RC**

| Role | AID | Notes |
|---|---|---|
| Requested stretch (tuner setting) | **85** | Multiplicand into `sub_4A94` |
| Incoming captured stretch | none (live proxy **149**) | `0x2005E8`; not TC0 |
| Applied stretch | **none** (computed) | TC0 operand after AID 13 |
| Backdown | **13** | Subtracted from the TC0 operand |
| RPM | **78** | Gate around 3200 RPM at the TC write; RPM piecewise scalars feed telemetry `0x200604`, not `sub_4A94` |
| Fuel telemetry | **148** | Parallel path, not TC0 |

`sub_4A94` does **not** load RPM `0x2005EC`. AID 85 is a clamp, not an RPM table. If the ECM already shortens pump stretch with RPM, AID 149 can fall while AID 85 stays put. That is still not live TC0 proof.

USB VID/PID commonly cited for the CDC device: `0x1A18` / `0x0002`, 921600 baud. **No Quadzilla USB device was on the bench in the 2026-08-22 pass.** Do not invent matrix cells.

## What the published GitHub README still gets wrong

[quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) is the public pointer. Its root README still carries older slogans (57/60 functions, 117 AIDs as if one profile, “complete RE”). Those numbers are **not** current truth.

Do **not** use `QUADZILLA_RE_COMPLETE.md` as current truth. Lab corrections include: 122 functions listed in `firmware_analysis_results.json` (not 57/60); `FirmwareUpdate.pwk` is 4 bytes `111d6f20`, not the full key; free flash is **2,888 bytes** at `0xB1B8`–`0xBCFF`, not 19 KB; no `DADR9802` / `Aug 2 2018` strings in this image; `FUN_00427401` is a PC-side decompressor, not MCU fueling; the 72-byte TPS island at `0xB1B8` has **no** stock xref (unused, not a live patch).

## Hardware-blocked / still unknown

These are open because there was no tuner on USB/BLE in that pass, not because the files were unread:

- Live AID read/write against a physical Adrenaline
- Converting TC0_RC (`applied*24+3`) to microseconds with a measured timer clock
- Filling a 1500–3000 RPM matrix (AID 85 vs 13 vs 148/149) with the engine running
- Analog TPS vs CAN TPS at `0x2005D7` / `0x200BC3`
- Probing unnamed firmware AIDs 10, 64, 80, 82, 151, 156–180 on device
- A runtime hook in `0xB1B8`–`0xBCFF` (no unused vector proven)
- USB flash opcodes remain **documentation-only** in the lab client (`quadzilla_aid_bench.py` does AID bench, not a verified flash programmer)

## How this relates to the CM551 dumps

Adrenaline can change **what the pump sees** relative to stock ECM tables. The CM551 5D fuel and 4D timing grids in [factory-fuel.md](factory-fuel.md) / [factory-timing.md](factory-timing.md) are the **ECM** calibration. AID 85 stretch is a **tuner** overlay. They are not the same parameter space. This master repo does not claim a numeric mapping from 5D MM3S cells to AID 85. Plain-language overlay notes: [quadzilla-vs-factory.md](quadzilla-vs-factory.md).

Do not mix CM551 ReadByNTN facts into Adrenaline ARM7 notes, or the reverse.

## DTC website

If you need human-readable Quadzilla/iQuad code text, the lab has `dtc_website/index.html` embedding the 1,258-row export. That is Adrenaline/iQuad DTC language, **not** the CM551 INSITE fault list from the bench (123, 144, 153, 211, 278, …).
