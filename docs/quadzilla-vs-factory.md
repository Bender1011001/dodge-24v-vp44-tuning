# Quadzilla Adrenaline vs factory CM551 maps

> **Docs:** [Home](../README.md) · [Fuel](factory-fuel.md) · [Timing](factory-timing.md) · [Adrenaline vs ECM](quadzilla-vs-factory.md) · [All 29 maps](maps.md) · [HTML viewer](../maps/tune_A_vs_B.html) · [Safety](safety.md)

This page is for someone who has (or is thinking about) a **Quadzilla Adrenaline** on a 24-valve VP44 Dodge and has just looked at the factory `5DFL` / `4DTA` tables in this repo. It is not a programming guide, not a power-level recipe, and not a copy of the Adrenaline firmware tree.

Firmware reverse-engineering: [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed). Verified-vs-stale summary: [quadzilla.md](quadzilla.md). Factory numbers: [factory-fuel.md](factory-fuel.md), [factory-timing.md](factory-timing.md).

Lab audit date for the ARM7 facts below: **2026-08-22**. Prefer that audit over older “complete RE” writeups.

## What Adrenaline is (and is not)

Adrenaline (DADR9802 class) is an **inline piggyback**. It is a separate ARM7 computer from the Cummins **CM551**. The CM551 still owns the KennPar maps in this repository (`5DFL*`, `4DTA*`, `FLFLTBZA`, `AFFLLMZA`, …). Adrenaline **does not rewrite those ITNs**.

What it *does* do, as a product and as firmware structure:

- It sits in the **ECM ↔ VP44** path.
- It **receives** ECM traffic (CAN RX / a capture stream unpacked in `sub_59E8`). Incoming **stretch** from that stream lands at SRAM `0x2005E8` — the ECM/wiretap measurement, not the tuner setting.
- It can **change what the pump is driven with** relative to that stock command. The closed static chain for **quantity** is pulse stretch on the AT91 timer, not a 5DFL cell edit.

Closed structural chain (Thumb, not a live VP44 bench proof):

**AID 85 (Maximum Fuel Stretch, µs) → working copy `0x200590` → clamp → `sub_4A94` → minus AID 13 (backdown %) → `sub_6FA0` TC0_RC (`applied × 24 + 3`)**

`AID 85` is a **clamp / requested stretch**, not an 11×18 RPM×fuel table. `sub_4A94` does **not** load RPM. If the ECM already shortens stretch with RPM (that is what factory `5DFL` / AFC are for), Adrenaline’s incoming capture can fall while AID 85 stays put.

There was **no Adrenaline on USB** in that audit. Do not invent a live RPM matrix or a microseconds-per-TC0-tick number.

## Factory KennPar → Adrenaline adjustment (effect, not cell math)

“Trying to achieve the effect of” means: these are the factory tables whose **job** the piggyback is substituting for or stacking on. It does **not** mean Adrenaline interpolates the same grid.

| Factory KennPar | Factory job (this dump) | Adrenaline analogue (Dodge 1998–2002 v2.7 profile + ARM7 map) | What we actually know |
|---|---|---|---|
| `5DFL00ZA` / `5DFL01ZA` | ECM fuel request vs throttle × RPM (mm³/s). A richer than B on the 100% row. | **AID 85** max stretch (µs); tap / TPS pump min–max (AID 18, 19, 110); **AID 113–136** boost-level fueling as **50–150%** of a base. | Quantity overlay is real as a **stretch path to TC0**. There is **no** proven formula from a 5DFL cell (mm³/s) to AID 85 (µs). AID 85 is not RPM-tabled. |
| `4DTA00ZA` / `4DTA01ZA` | ECM timing vs fuel × RPM (DEG). Same A and B. Transient table retards hard 1280–2800 RPM at load; steady-state stays advanced. | iQuad **Timing Parameters** (AID 17, 59–62) and **RPM Timing Max** equalizer (AID **137–141**, 1500 / 2000 / 2500 / 3000 / Max, DEG). | Those AIDs are **named** timing in the profile. The audited stretch chain does **not** close them to a pump timing command. **Unknown** whether they move VP44 timing, clamp a display, or do something else. |
| `FLFLTBZA` | Convert fuel units → mg/stroke. Same A and B. | None in the Dodge 2.7 profile that maps to this table. | Overlay happens **after** the ECM has already built a pump command. No evidence Adrenaline patches `FLFLTBZA`. Treat conversion as ECM-internal. |
| `AFFLLMZA` | AFC fuel **limit** vs boost (INHG) × RPM. Truncated; axes differ A vs B; A’s ceiling is much higher at low boost. | **AID 113–136** (% fuel vs PSI boost); **AID 13** backdown from boost/threshold walk; **AID 81** boost defuel PSI. | Same *job* (less fuel when boost is low / too high), different computer and units (INHG table vs PSI percent). **No** cell-for-cell mapping. |
| `ATFLLMZA` | Altitude derate vs ambient × RPM. On **both** of these boxes every cell is **400** mm³/s — a high ceiling, not an active cut vs 5DFL ~110. | No Dodge 2.7 AID we can honestly call “altitude derate.” | Nothing to harmonize on these two cals. Do not invent an Adrenaline altitude table. |

### AID 149 (do not trust the iQuad caption)

iQuad labels AID **149** as **“Timing”** in DEG. The ARM7 map says AID 149 is a **scaled copy / live proxy** of incoming captured stretch (`0x2005E8`) and of telemetry word `0x200604`. That word’s consumers are pack/snapshot, **not** `TC0_RC`. Correlation is not a timing-advance proof. Use [quadzilla.md](quadzilla.md) and the Quadzilla repo, not the gauge name.

## How a human would *think* about factory 5DFL / 4DTA under Adrenaline

This is overlay hygiene, not a “how to write the ECM” procedure. This repository will not tell you how to program a CM551.

### Fuel (`5DFL`)

The 100% row is the factory **full-throttle request** the ECM computes before (or as) it talks to the pump. Adrenaline then applies **stretch** (AID 85 and friends) and **percent-of-base vs boost** (AID 113–136).

- If Adrenaline is already adding fuel, **raising 5DFL as well is stacked fuel**, not an either/or. Smoke, EGT, and pump stress add; they do not replace each other.
- **A (J90269.06) is already the richer factory 5DFL**, especially at 2800–3000 RPM. The same AID 85 on A starts from a higher ECM request than on B (J90268.04).
- Part-load 5DFL (0 / 25 / 50) is the same on A and B. Cruise/light-load behavior is not the A-vs-B story; WOT is.
- **Do not “max 5DFL” as a default** just because Adrenaline is installed. Decide which computer is supposed to make the extra fuel: the ECM table, the piggyback stretch, or a little of both — and live with the sum.

**Unknown:** whether the stretch Adrenaline captures is **before or after** factory `AFFLLMZA` / `ATFLLMZA`. If AFC is applied in the ECM first, B’s tight low-boost limiter (about **45 mm³/s** from 1280 RPM at 0 inHg) still caps what the piggyback sees. If Adrenaline stretches a pre-AFC quantity, factory AFC may not save you. We have not proven the order.

### Timing (`4DTA00` vs `4DTA01`)

Factory timing is **two maps**, not one. They match A vs B, so silk-screen is not your timing choice — **transient vs steady-state** is.

- `4DTA00ZA` (transient) has a **retard hole** from about 1280–2800 RPM at mid/high fuel (cells down to about **−6.3 DEG**).
- `4DTA01ZA` (steady-state) stays **positive** in that band (about **+4 to +8 DEG**).
- Y is **fuel mm³/s**, not 5DFL throttle %. The top Y breakpoints also differ (90 / 98 vs 85 / 93).

If Adrenaline’s timing AIDs *do* add degrees (unproven at the pump), adding advance on top of a **already-retarded transient cell** is a different truck than adding the same offset on top of steady-state +5°. Watch **00 vs 01**, not “the timing table.”

**Unknown:** Adrenaline’s exact timing cell math. Do not interpolate AID 137–141 onto 4DTA columns and call it a decode.

### Conversion (`FLFLTBZA`)

Same on A and B. Leave it unless you have a specific conversion/density reason. It is not a substitute for 5DFL, and Adrenaline is not known to implement it.

### AFC (`AFFLLMZA`)

Factory A on the sampled complete rows has an AFC ceiling **well above** 5DFL (so 5DFL is the request that bites first at high boost). Factory B is **much tighter at low boost**. Adrenaline’s 113–136 curve is a **percent vs PSI** overlay on *its* fuel path. Running 150% boost-level fueling on a box whose factory AFC is already the tight B table is not the same as doing it on A. We still lack order-of-operations proof.

The `AFFLLMZA` Z dump is incomplete (512/588 bytes). Do not retune AFC from a truncated grid.

## What we do not have yet (leave these unknown)

- Live AID read/write against a physical Adrenaline (no USB device on the 2026-08-22 pass).
- TC0 ticks converted to microseconds with a measured timer clock.
- A filled 1500–3000 RPM matrix (AID 85 vs 13 vs 148/149) with the engine running.
- A numeric map from `5DFL` mm³/s cells → AID 85 µs, or from `4DTA` DEG cells → AID 17/137–141.
- Proof that iQuad “Timing” (AID 149) is injection timing. Static chain says it is not TC0.
- Proof that AID 137–141 command the VP44.
- Whether Adrenaline intercepts pre-AFC or post-AFC quantity.
- The missing 38 `AFFLLMZA` cells.

## Pointers (no binaries copied here)

| What | Where |
|---|---|
| Factory fuel / timing numbers | [factory-fuel.md](factory-fuel.md), [factory-timing.md](factory-timing.md) |
| Adrenaline RE summary for this truck family | [quadzilla.md](quadzilla.md) |
| Firmware, AID tables, x2com | [quadzilla-adrenaline-reversed](https://github.com/Bender1011001/quadzilla-adrenaline-reversed) |
| Read-only CM551 puller | [cm551-i6pull](https://github.com/Bender1011001/cm551-i6pull) |

Do not copy Adrenaline `.qz` / ARM7 images, the PC updater, or the iQuad APK into this master repo. Do not treat this page as a flash or AID-write tutorial.
