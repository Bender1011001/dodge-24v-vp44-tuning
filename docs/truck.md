# The truck, the ECM, and the wire

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

## What this vehicle is

A Dodge Ram with the **24-valve 5.9 Cummins** (ISB family), Bosch **VP44** rotary injection pump, and a Cummins **CM551** engine control module. In Chrysler terms this is the late-1990s / early-2000s 24-valve Cummins, commonly dated **1998.5 through 2002**.

The CM551 is the engine computer. It is not the Chrysler body/PCM. On these trucks the engine box talks to the pump on a dedicated Cummins datalink, and also talks (when present) to the Chrysler side over a separate PCM datalink. Bench captures here were key-on, engine stopped, with sensors unplugged; INSITE then reported expected sensor and PCM-link faults. Those faults are a bench condition, not a driveability diagnosis.

Two physical CM551 housings were read. They share ECM part number `03942336` and ROM date `091197`. They do **not** share the silk-screened calibration code or the calibration date. See [cm551.md](cm551.md).

## VP44 and the ECM

The VP44 is an electronically timed / metered rotary pump. The ECM computes fueling and timing and sends commands to the pump. The pump is not a J1939 peer in the SAE-truck sense on this application: the live 11-bit frames on the 3-pin Cummins connector are the ECM↔VP44 conversation, at **250 kbps**, standard (11-bit) CAN identifiers.

Observed idle 11-bit traffic (listen only; periods ~60 ms):

| ID | Example data (bench) |
|---|---|
| `0x112` | `0C 00 00 00 00 00 6A/6E 12` |
| `0x512` | `00 00 00 00 00 00 98/94 02` |
| `0x001` | `00 00 00 00 00 AA 01 00` |
| `0x500` | `F8 02 00 00 16 01 42 01` |

Those IDs are **not** a diagnostic API. They are pump/ECM operational frames. This project never transmits them. Sending tester traffic on `0x112` / `0x512` / `0x001` / `0x500` would be fueling-path interference.

## The 3-pin Cummins datalink is not J1708

Cummins service literature for other eras uses J1708/J1587 (MID 128, etc.). This bench cable is the Dodge **3-pin Cummins datalink**. On this truck that wire is **CAN at 250 kbps**, not J1708.

What was verified live:

- INLINE 6 USB, RP1210 device **254**, vendor DLL `CMNSI632.dll`.
- INSITE autoconfigure: USB J1939 succeeded, USB J1708 failed.
- A J1708 RP1210 session connected and echoed the tool; there was **no** ECM MID 128 traffic.
- A J1939 RP1210 session at 250 kbps also connected. Until receive was enabled it looked dead. After receive was enabled it showed **only the tool’s own 29-bit TX looped back**. No ECM address claim, no VIN PGN, no EF00 replies on that stack.
- Opening the same channel as raw **`CAN:Baud=250,Channel=1`** produced hundreds of frames in a few seconds: **11-bit VP44 IDs plus 29-bit CPP/J1939-style IDs on the same wire**.

So: the physical plant is mixed CAN. J1708 is the wrong layer for this connector. A “J1939” RP1210 session is the wrong filter for the 11-bit traffic, and on this adapter it also failed to deliver the 29-bit diagnostic replies. The working diagnostic path is raw CAN, 250 kbps, channel 1, with the tool speaking 29-bit Proprietary A (`PGN EF00`) beside the pump’s 11-bit frames.

## Why INSITE said J1939

INSITE’s adapter picker labels the session **USB J1939**. That is the INLINE protocol name, not a statement that the Dodge 3-pin wire is a textbook SAE J1939 vehicle backbone.

On the wire:

- 11-bit IDs belong to the VP44 link.
- 29-bit IDs (priority 6, PGN `EF00`, destination 0, source `0xF9` for the tool) are the Cummins proprietary parameter protocol (CPP / ReadByNTN). Transport uses J1939-style TP.CM / TP.DT (`PGN EC00` / `EB00`).

INSITE reached the box because **29-bit CPP rides next to the 11-bit pump frames**. The UI string “J1939” is how the service tool asked the INLINE firmware to talk. It is not ISO 15765-4 UDS, and it is not a J1708 ECM.

ISO15765 at 250 kbps on the same channel connected with **zero RX** while idle. There is no tester-initiated UDS session sitting on the bus waiting. Do not look for a 29-bit diagnostic stack by requesting VIN on `FEEC` through the J1939 RP1210 protocol string; that path was tried and produced no ECM frames.

## Adapter facts that matter on this truck

- Close INSITE (and any other INLINE client) before another program claims device 254. The adapter is exclusive.
- `CMNSI632.ini` on this PC is **`RP1210=B`**. `RP1210_ReadMessage` is `(client, buffer, size, blocking)`. Passing a timeout as the second argument hangs the DLL.
- Receive stays empty until **`RP1210_SET_MESSAGE_RECEIVE` (command 18)** with data `01`.
- Key-on is enough. This is not a running-engine interface and must not be used as one.

Protocol detail for the KennPar read is in [protocol.md](protocol.md). Safety constraints are in [safety.md](safety.md).
