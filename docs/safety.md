# Safety

This repository is **read-only documentation** plus **read-only KennPar captures** from two CM551 modules the owner already possessed. Nothing here is a programming file.

## Do

- Use I6Pull or INSITE as an **upload / service** path if you own the hardware and the adapter.
- Close INSITE before running I6Pull (exclusive adapter).
- Keep work at key-on, engine stopped, unless you are doing a documented listen-only capture.
- Treat `maps/*.json` as study data. VIN at ITN `81AC` is redacted; do not try to reconstruct it.

## Do not

- **Program, download-to-ECM, flash, erase, or jump to bootloader.** This writeup will not tell you how. I6Pull will not do it.
- **Transmit VP44 11-bit IDs** `0x112`, `0x512`, `0x001`, `0x500`. Those are ECM↔pump fueling frames. Listen only.
- **Request password ITNs** (`ADJPSWD1`–`6`, `ECM_PSWD`, `OEM_PSWD`, `DPFLPSWD`) or **BOOTDST / boot-copy** (`11AF` and related). They are omitted from the published dumps on purpose.
- Use this tool stack as a **running-engine fueling interface**.
- Copy Calterm metafiles, INSITE DLLs, UDC Pro databases, or Smarty firmware into a public tree. This repo does not.

I6Pull’s blocked ITN list: `0005`, `0016`, `001E`–`0022`, `1083`, `11AF`, `1267`.

## What the files are not

| File | Not |
|---|---|
| `maps/A_dump.json` / `B_dump.json` | Flash, ROM, INCAL, `.xcal`, or a brick-recovery image |
| `maps/tune_A_vs_B.html` | A writable calibration |
| INSITE `.eif` (not in this repo) | A flash dump |
| Quadzilla `.qz` / Smarty `.Smt` (not in this repo) | Something to confuse with CM551 KennPar |

Bricking a 25-year-old CM551 or a VP44 by experimenting with write/bootloader commands is easy and out of scope. Read the maps. Do not program the box from this repository.
