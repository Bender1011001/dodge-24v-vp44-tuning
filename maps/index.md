# Maps

> **Docs:** [Home](../README.md) · [Fuel](../docs/factory-fuel.md) · [Timing](../docs/factory-timing.md) · [Adrenaline vs ECM](../docs/quadzilla-vs-factory.md) · [All 29 maps](../docs/maps.md) · [Safety](../docs/safety.md)

## Open first (markdown, shop tables)

| Page | Contents |
|---|---|
| [docs/factory-fuel.md](../docs/factory-fuel.md) | `5DFL00ZA` / `5DFL01ZA` A and B, 100% deltas, `FLFLTBZA`, truncated `AFFLLMZA`, flat `ATFLLMZA` |
| [docs/factory-timing.md](../docs/factory-timing.md) | `4DTA00ZA` / `4DTA01ZA` (A = B), transient retard vs steady-state advance |
| [docs/quadzilla-vs-factory.md](../docs/quadzilla-vs-factory.md) | Adrenaline overlay vs those KennPars |
| [docs/smarty-s03-maps.md](../docs/smarty-s03-maps.md) | 1998 UDC stock vs factory A/B (`FLFL` / `4DTA` / `5DFL`) |

## Full 29-map viewer

Open [tune_A_vs_B.html](tune_A_vs_B.html) in a browser. Amber cells differ. Dark layout on purpose.

The HTML is index-aligned. That is fine for `5DFL` and `4DTA`. For **`AFFLLMZA`**, A and B **RPM/boost axes differ** — use the fuel page’s same-breakpoint slices, not HTML column index.

## Files in this folder

| File | Contents |
|---|---|
| [tune_A_vs_B.html](tune_A_vs_B.html) | Decoded maps and scalars, A vs B |
| [tune_A_vs_B.json](tune_A_vs_B.json) | Same decode as JSON |
| [tune_preview.md](tune_preview.md) | Older compact preview (superseded for shop use by the factory pages) |
| [DIFF.md](DIFF.md) | Short cal vs runtime summary |
| [A_identity.json](A_identity.json) / [B_identity.json](B_identity.json) | Identity without vehicle id / engine serial |
| [A_dump.json](A_dump.json) / [B_dump.json](B_dump.json) | Packed ITN dumps; vehicle-id ITN redacted |
| [smarty/](smarty/) | 1998 UDC decoded grids + [s03_vs_factory.html](smarty/s03_vs_factory.html) |

Decode rules and the other 24 Z-maps: [docs/maps.md](../docs/maps.md).
