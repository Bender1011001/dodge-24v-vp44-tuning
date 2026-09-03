# A vs B — calibration vs runtime

Two CM551 KennPar dumps, same ECM P/N `03942336` / ROM `091197`. Packed ITN blobs compared after VIN redaction.

| | A (J90269.06) | B (J90268.04) |
|---|---|---|
| Cal date | 062800 | 102198 |
| Engine hours | 13130:48:02 | 10196:32:59 |
| Key-on | ~13724 | ~10240 |
| ECM VSS miles | ~81 | ~287919 |
| ITNs in dump | 667 | 667 |

## Counts

- Identical ITN payloads: **536**
- Differing ITN payloads: **130** after VIN redaction (**131** in the raw capture, including ITN `81AC`)
- Decoded map tables that differ: **2** (5DFL00ZA, 5DFL01ZA)

Raw blob diffs include runtime counters (hours, key-on, VSS miles) and trailing bytes past some KennPar tables. A differing ITN blob does not always mean the decoded map differs.

## Fuel and timing

- `4DTA00ZA` ITN 1041: decoded 11 × 18, table matches
- `4DTA01ZA` ITN 103E: decoded 11 × 18, table matches
- `5DFL00ZA` ITN 1059: decoded 4 × 18, table DIFFERS
- `5DFL01ZA` ITN 1056: decoded 4 × 18, table DIFFERS
- `FLFLTBZA` ITN 8014: decoded 15 × 15, table matches

- `FLFLTBZA` conversion table: raw blob **matches**
- 4D timing axes (`4DTA00XA` / `4DTA00YA`): **match** / **match**
- `4DTA00ZA` (`1041`): first raw-byte diff at **480** (blob 512 bytes). Axis prefix is **11 × 18** (Y × X); 18×11×2 = 396, so a diff at byte 480 is **past the table**.
- `5DFL00ZA` (`1059`): first raw-byte diff at **114**. Axis prefix **4 × 18**. Catalog comment says 17×4; first u16 is byte length of points.
- `5DFL01ZA` (`1056`): first raw-byte diff at **114**.

## Cal-ish ITNs that differ

- `0003` CAL_DATE (6 / 6 bytes) first diff byte 0
- `0006` DAT_PLAT (818 / 818 bytes) first diff byte 7
- `001D` DATADATE (6 / 6 bytes) first diff byte 0
- `1041` 4DTA00ZA (512 / 512 bytes) first diff byte 480
- `1056` 5DFL01ZA (512 / 512 bytes) first diff byte 114
- `1059` 5DFL00ZA (512 / 512 bytes) first diff byte 114
- `801D` FLCKSPTM (12 / 12 bytes) first diff byte 1

## Runtime / identity ITNs that differ

Hours, key-on, VSS miles, and similar live counters. VIN (`81AC`) is redacted on both sides and is not compared.

- `0004` CMECTR (4 / 4 bytes) first diff byte 0
- `001C` HOUR_MTR (4 / 4 bytes) first diff byte 0
- `1231` PREFAULT (100 / 100 bytes) first diff byte 0

## Other differing ITNs

- `0008` ADBS01 (174 / 174 bytes) first diff byte 20
- `000F` DGBISW01 (16 / 16 bytes) first diff byte 14
- `0024` DGFUCATB (1536 / 1536 bytes) first diff byte 533
- `0025` DG0000CB (1000 / 1000 bytes) first diff byte 3
- `0026` DGFUIDEN (56 / 56 bytes) first diff byte 4
- `1003` ADADG1CA (600 / 600 bytes) first diff byte 107
- `1004` ADADG1FT (546 / 546 bytes) first diff byte 3
- `1005` DCBFCEAD (26 / 26 bytes) first diff byte 3
- `100C` CMLSEL (878 / 878 bytes) first diff byte 25
- `1031` DGFUCUBF (4688 / 4688 bytes) first diff byte 40
- `1036` ADICDTER (100 / 100 bytes) first diff byte 69
- `1044` SSEECRC (2 / 2 bytes) first diff byte 0
- … 108 more

Decoded view: [tune_A_vs_B.html](tune_A_vs_B.html).
