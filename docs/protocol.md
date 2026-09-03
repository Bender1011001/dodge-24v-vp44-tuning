# ReadByNTN protocol (CM551, Dodge 3-pin CAN)

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [Safety](safety.md)

Facts for the KennPar pull used by [I6Pull](https://github.com/Bender1011001/cm551-i6pull). The tool **only reads**. This page is the distilled wire protocol, not a lab diary and not a CureCore decompile.

Companion: [cm551-i6pull/docs/protocol.md](https://github.com/Bender1011001/cm551-i6pull/blob/master/docs/protocol.md).

## Bus

Dodge 3-pin Cummins datalink, **250 kbps** CAN, mixed:

- 11-bit VP44 pump traffic (listen only)
- 29-bit CPP / J1939-style traffic (this puller)

I6Pull never transmits 11-bit IDs `0x112`, `0x512`, `0x001`, or `0x500`. See [truck.md](truck.md) for why a J1939 RP1210 session was the wrong way to see this bus.

## INLINE 6 / RP1210B

| Item | Value |
|---|---|
| DLL | 32-bit `CMNSI632.dll` (`SysWOW64` on 64-bit Windows) |
| Device | **254** (`INLINE6,USB`) |
| INI | `RP1210=B` |
| Connect string that worked | `CAN:Baud=250,Channel=1` |
| CAN format | **4** |
| Tool address | `0xF9` (off-board diagnostic) |
| Engine address | `0x00` |

`RP1210_ReadMessage` argument order on this DLL (RP1210**B**):

```
ReadMessage(clientId, buffer, size, blocking)
```

buffer, then size, then blocking. Passing a timeout as the second argument made the DLL treat `5` as a pointer and **hang**. Blocking **0** (poll) is what I6Pull uses.

Receive is off until the client sends **`RP1210_SET_MESSAGE_RECEIVE` (command 18)** with data `01`. Without that, TX can succeed (`rc=0`) with **zero RX**. Echo-TX (command 16) was used while debugging; the working pull still requires SET_MESSAGE_RECEIVE.

Firmware reported via `ReadDetailedVersion` on this adapter: API 3.0, DLL **6.8.1.0**, FW **6.66**. Close INSITE first; it holds the adapter exclusively.

A 64-bit Python process cannot load the 32-bit DLL. I6Pull is C# / .NET 4 **x86**.

## Read request — command `0x48`

Tool TX CAN ID: **`0x18EF00F9`**  
(priority 6, PGN `EF00` Proprietary A, dest 0, src `F9`).

11-byte payload:

```
48 | NTN_be | offset_be | length_be
```

- `48` — ReadByNTN
- NTN / ITN as `u16` **big-endian**
- offset `u32` BE (0 for a full parameter)
- length `u32` BE (bytes requested)

Eleven bytes does not fit in a single 8-byte CAN frame, so the tool uses J1939 transport (peer TP, not BAM broadcast):

| Role | CAN ID | Meaning |
|---|---|---|
| Tool RTS | `0x18EC00F9` | start of request |
| Tool DT | `0x18EB00F9` | request bytes |
| ECM RTS | `0x18ECF900` | start of reply (`10` … size … packets … `FF` … PGN EF00) |
| Tool CTS | `0x18EC00F9` | windows of **32** packets |
| ECM DT | `0x18EBF900` | reply bytes |

Reads longer than **1024** bytes are split into chunk requests (offset/length). Several tables in this catalog are 512-byte KennPar blobs even when a comment implies a larger grid (`AFFLLMZA` is the example: 512 dumped of 588 needed).

## Reply — command `0x49`

Envelope:

```
49 | NTN_be | offset_be | length_be | data
```

I6Pull strips the 11-byte header and logs the data bytes.

Negative response seen on this Dodge cal: payload starting **`0D 08 48`**. The decoder treats that as NAK (parameter not readable / not present), not as table data. Hybrid-governor maps and several heater/torque maps NAK; see [maps.md](maps.md).

## What is not sent

The same proprietary PGN family in the service-tool binary includes other command bytes (lab notes mention `0x43`, `0x46`, `0xFF`, and `FE FE` service). This project **does not classify or send** those. I6Pull’s allow-list is read `0x48` only.

Also never sent from this tool:

- erase / prepare-cal-download / run-boot-loader
- write-scratch / jump-absolute
- VP44 11-bit frames
- password ITNs and BOOTDST (`11AF` and the ADJPSWD family)

Blocked ITNs in I6Pull: `0005`, `0016`, `001E`–`0022`, `1083`, `11AF`, `1267`.

## Catalog

`catalog/chr0000_reads.csv` in the i6pull repo lists ITN hex, byte length, and names for the 667-parameter pull. That is a **readable subset** of the Dodge E2M, not the full 5k+ KennPar list. The E2M files themselves are copyrighted metafiles and are not in this master repo.

NTN endianness on the wire is **big-endian**. `DATADATE` ITN `001D` is the sanity check.

## How this was established (short)

INSITE already implements `J1939CPPReadByNTNRequest`. The on-wire shape (command `0x48`, BE NTN, two BE dwords) was confirmed **live** on this truck: identity ITNs first, then the 667-ITN catalog on both boxes. Service-tool internals (MBA-flattened packers, RTTI names) are not required to *use* the read path and are not reproduced here.

Standard J1939 PGNs (VIN `FEEC`, hours `FEE5`, DM1, …) were **not** the working identity path on the J1939 RP1210 session. Identity came from ReadByNTN on raw CAN.
