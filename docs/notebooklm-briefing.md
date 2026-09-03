# Two factory tunes on the 24-valve Cummins

A spoken briefing for NotebookLM. Write the audio overview from this narrative. Use complete sentences. Speak numbers. Do not read tables cell by cell. Do not recite VIN, engine serial, passwords, or bootloader material — none of that belongs in this story.

## What to upload (human — skip this in the audio)

You already uploaded the factory A-versus-B PDF and the GitHub README. Add these extra GitHub files. The packing list is not the show; start the overview with the trucks.

**Add**

- This briefing: `docs/notebooklm-briefing.md`
- `docs/factory-fuel.md`
- `docs/factory-timing.md`
- `docs/quadzilla-vs-factory.md`
- `docs/truck.md`
- `docs/safety.md` (short)

**Optional** (detail, not the spoken spine)

- `docs/smarty-s03-maps.md`
- `docs/protocol.md`
- `docs/maps.md`

**Skip**

- `maps/tune_A_vs_B.html` and `maps/factory-a-vs-b.html` (huge Plotly pages; the PDF already has the charts)
- Dump JSON (`maps/tune_A_vs_B.json`, `maps/A_dump.json`, `maps/B_dump.json`, and every-cell JSON)
- Vendor blobs: any `.dat`, `.Smt`, or `.e2m`

If a fuel or timing page disagrees with a spoken figure below, trust the decoded cells on those pages. This briefing is the story those cells tell.

---

## The trucks, and why factory maps still matter

These are Dodge Rams with the twenty-four-valve 5.9 liter Cummins, Bosch VP44 injection pump, and Cummins CM551 engine controller. Common model years are 1998.5 through 2002. The CM551 is the engine computer, not the Chrysler body controller. It computes fueling and timing and sends commands to the pump on a dedicated Cummins datalink. The VP44 is an electronically timed and metered rotary pump. Quantity and timing live in the ECM, then on the wire to the pump.

Those trucks are old enough that the aftermarket grew a whole language around them. Quadzilla Adrenaline is a piggyback on the ECM-to-pump path. Smarty is a handheld with its own software families. Hardware, pumps, and service-tool licenses for this era are getting scarce. A working CM551 is not a disposable module. That is why two factory calibrations, captured from boxes the owner already had, are worth sitting with. The publication is for reading what those controllers already contain. It is not an invitation to go hunting for Cummins calibration packages, and it is not a substitute for Cummins or Chrysler service tools.

## The hook: two boxes, same ROM, different fuel

The owner had two physical CM551 modules. They share part number 03942336, spoken as oh-three-nine-four-two-three-three-six. They share ROM date 091197, which is September 11, 1997. They are not the same calibration.

Call them A and B, because that is how the dumps are named, and because this project does not publish VIN or engine serial.

Box A is silk-screened J90269.06. Its calibration date is 062800, June 28, 2000. The dataplate reads like a 6BTA 5.9, fuel-pump code FP98455, Chrysler T-300. Box B is silk-screened J90268.04. Its calibration date is 102198, October 21, 1998. The plate reads like an ISB 235, pump 98453, Chrysler automotive.

Timing tables match. Fuel tables do not. Same part number, same ROM stamp, two different factory fuel requests at wide-open throttle. That is the episode.

Give the boxes character from identity fields that are safe to say out loud. Engine hours and ECM vehicle-speed miles are runtime counters stored in the controller, not photographs of an odometer. Box A reports about thirteen thousand one hundred thirty-one hours and only about eighty-one ECM VSS miles. Box B reports about ten thousand one hundred ninety-seven hours and about two hundred eighty-seven thousand nine hundred nineteen ECM VSS miles.

The mile contrast is the kind of detail a two-host show will grab, and it should stay honest. Eighty-one miles next to thirteen thousand hours is consistent with a box that ran a long time without a vehicle-speed input the ECM trusted, or with a module that did not spend its whole life in the truck that currently holds it, or with a difference in how VSS is counted. This writeup does not turn those two numbers into a vehicle history. Hours and miles are not the fuel map.

## How the maps came off the hardware

The pull was read-only, key-on, engine stopped. A Cummins INLINE 6 sat on the Dodge three-pin Cummins datalink. That wire is CAN at two hundred fifty kilobits per second, mixed: eleven-bit frames for the VP44 pump conversation, and twenty-nine-bit Cummins proprietary parameter traffic riding next to them. The eleven-bit IDs are not a diagnostic API. This project listens and does not transmit them.

The engineering read is ReadByNTN, command 0x48. Both boxes answered a six hundred sixty-seven parameter catalog with zero misses: 667 of 667. Roughly half a minute per module. What came back is a dictionary of parameter payloads decoded to engineering units. It is not a flash image, and it is not a file you program onto another ECM.

That is all the protocol the overview needs.

## How to hear the units

Three unit systems show up. Mash them together and the story goes muddy.

Fuel request in the 5DFL tables is cubic millimeters per second. When this briefing says A is richer, it means a higher cubic-millimeter-per-second request versus throttle and RPM, not a horsepower sticker on a shop wall.

A separate table, FLFL, converts those fuel units toward milligrams per stroke. That is conversion, density-style, not the throttle-to-fuel request. Changing conversion without changing 5DFL is a different kind of edit than raising the full-throttle fuel row.

Timing in the 4DTA tables is degrees. Positive is advance. Negative cells in the transient table are real retard, not a decode bug.

Both fuel and timing come in a pair. The 00 table is transient. The 01 table is steady-state. They are not copies of each other. On 5DFL, the Y axis is throttle percent: zero, twenty-five, fifty, and one hundred. On 4DTA, Y is commanded fuel in cubic millimeters per second, not those throttle rows. Do not line the tables up by row number and call it the same load.

Decoded numbers are already in engineering units. Speak those. Fuel X starts at six hundred RPM; timing X starts at seven hundred. On these boxes 5DFL is four by eighteen and 4DTA is eleven by eighteen.

## The difference: A asks for more fuel at full throttle

Part throttle is not the A-versus-B story. The zero, twenty-five, and fifty percent rows of both 5DFL tables match between the two boxes. Cruise and light load are the same factory request.

The one hundred percent row is the complete, trustworthy calibration delta. From about twelve hundred RPM up, A is richer in the mid and high columns. Through the teens and low two-thousands the gap is a few cubic millimeters per second. It opens in the high two-thousands. It is largest at three thousand RPM.

Speak this pair. Transient fuel, 5DFL00, three thousand RPM, full throttle: A is about one hundred ten cubic millimeters per second; B is about ninety. A is about twenty cubic millimeters per second richer. The decoded cells are 109.987 versus 90.014, a difference of 19.973.

Steady-state fuel, 5DFL01, same speed and throttle: A is again about one hundred ten; B is about eighty-seven. A is about twenty-three cubic millimeters per second richer. Decoded: 109.987 versus 87.296, a difference of 22.691.

Two thousand eight hundred RPM is the other headline. Transient A holds near one hundred nine while B is near ninety-seven, about twelve cubic millimeters per second richer on A. Steady-state is the same shape, a little more than thirteen. At thirty-two hundred fifty RPM the 100 percent cells match again. The thirty-eight hundred column is zero on both. That is an unused high breakpoint, not a driveable fueling point.

In the truck that means calibration A requests more fuel at wide-open throttle in the mid and high RPM. Injection timing, as the next section says, did not change with the silk-screen. More requested fuel. Same timing tables. That is a richer factory WOT, not a different advance map wearing a diesel name.

If a piggyback is already adding fuel on top of the ECM command, A starts that overlay from a higher request than B. Stacking is addition. Smoke, exhaust temperature, and pump stress add. They do not cancel.

## What did not change

The 4DTA timing grids are identical on A and B once decoded. Silk-screen is not your timing choice. Transient versus steady-state is.

The useful contrast lives inside one box. Below about twelve hundred RPM both timing tables advance several degrees as fuel rises. From twelve hundred eighty RPM through about twenty-eight hundred, the transient table goes negative at mid and high fuel, about minus two to minus six point three degrees. The steady-state table stays positive in the same band, about plus four to plus eight. The hole bottoms out at minus 6.328 degrees, including at twenty-seven hundred RPM. At three thousand and above, both tables come back positive.

If the overview keeps one timing fact, keep that hole. A truck still on the transient map is retarded on purpose in the meat of the power band. The same truck, settled into steady-state, is advanced. An overlay that also tries to add degrees is standing on two different floors depending on which table is active.

The conversion table FLFL matches on A and B. It is not a substitute for 5DFL.

Altitude derate matches too. On these two boxes every decoded cell is four hundred cubic millimeters per second. That is a high ceiling, not an active cut against a 5DFL request that tops out near one hundred ten. There is no altitude story to dramatize here.

The catalog lists twenty-nine Z-maps. A lot of them NAK on this Dodge calibration: hybrid governor, several heater and torque maps, and others that are simply not implemented on this application. Of the maps that actually decoded, most are the same on A and B. The complete differences that matter for driving are the two 5DFL fuel tables. Boost AFC is a third difference, with an asterisk.

## The AFC asterisk

AFFLLMZA is the factory smoke and boost limiter: a fueling ceiling versus boost in inches of mercury and RPM. It is not the 5DFL request. It differs on A and B. Be honest about how much is known.

The dump is truncated. The table is declared fourteen by twenty-one. The Z parameter returned 512 of 588 bytes, which is 256 of 294 cells. The last rows are incomplete. Do not treat the full grid as known.

The axes are not the same. A has a seven hundred RPM breakpoint; B has forty-five hundred instead. Boost breakpoints differ too. Column two of A is not the same engine speed as column two of B. Compare by physical RPM and boost, not by column index.

Where the dump can compare at the same breakpoints, A is the richer limiter. At zero boost, B falls to about forty-five cubic millimeters per second from twelve hundred eighty RPM up. A holds about seventy-four. At about twenty inches of mercury, still a light-boost row, A sits near one hundred sixty-four across most of the RPM axis, already above any 5DFL 100 percent cell. B is lower and shaped with RPM. On the sampled complete rows, A's AFC ceiling is well above 5DFL, so the fuel request is what bites first at high boost. B's AFC is much tighter at low boost.

That is a real third difference. It is also incomplete. Say both.

## Quadzilla Adrenaline: overlay, not a rewritten table

Quadzilla Adrenaline is a piggyback. It is a separate ARM7 computer from the Cummins CM551. The CM551 still owns the KennPar maps in this repository. Adrenaline does not rewrite those tables. It sits in the ECM-to-pump path, sees what the stock computer commanded, and can change what the pump is driven with. Quantity, on the audited firmware chain, is pulse stretch on a timer, not a 5DFL cell edit.

When people ask which factory tables it is trying to achieve the effect of, this is the honest pairing.

For 5DFL, the analogue is maximum fuel stretch in microseconds, plus throttle and tap limits, plus boost-level fueling as a percent of a base. The overlay is real as a stretch path. There is no proven formula from a 5DFL cell in cubic millimeters per second to that stretch in microseconds. Stretch is not an RPM-by-throttle grid the way 5DFL is.

For 4DTA, the analogue is the named timing parameters and the RPM timing-max equalizer. Those settings are named timing in the product profile. The audited stretch chain does not close them to a pump timing command. Unknown whether they move VP44 timing, clamp a display, or do something else. One iQuad caption that says "Timing" is a scaled copy of incoming captured stretch, not a proof of injection advance.

For FLFL, there is no Dodge 2.7 analogue. Overlay happens after the ECM has already built a pump command. Treat conversion as ECM-internal.

For AFC, Adrenaline has percent fuel versus PSI boost, plus backdown and boost defuel. Same job, different computer, different units. No cell-for-cell mapping.

Altitude on these two factory boxes is that four-hundred ceiling. There is nothing to harmonize.

What we do not know belongs in the show. There is no 5DFL-to-microsecond formula. The order of overlay versus factory AFC is unknown. If AFC is applied in the ECM first, B's tight low-boost limiter still caps what the piggyback sees. If Adrenaline stretches a pre-AFC quantity, factory AFC may not save you. We have not proven the order. A 2026 firmware audit is the source for the ARM7 facts; there was no Adrenaline on USB in that pass, so there is no live RPM matrix to invent.

If Adrenaline is already adding fuel, raising 5DFL as well is stacked fuel. A is already the richer factory 100 percent row. Decide which computer is supposed to make the extra fuel, and live with the sum. This repository will not tell you how to program a CM551.

## Smarty is a different product

Smarty is a handheld ecosystem with a PC side called UDC. It uses some of the same KennPar names, which is why tuners already recognize FLFL, 4DTA, and 5DFL. It is not Adrenaline, and it is not this dump.

The UDC year-stock `.dat` files are stock calibrations labeled by year and transmission. They are not the handheld software levels SW0 through SW9. The 1998 stock files decode to valid fuel, timing, and conversion tables. They are still not a Smarty power setting.

Handheld levels do not appear in the `.Smt` firmware as FLFL, 4DTA, or 5DFL grids. Until a CaTCHER slot is decoded into those same physical tables, there is no honest per-SW cell delta versus factory A or B. A horsepower claim on a sales page is not a map.

The next experiment in this project is already named: the owner will flash SW6, then SW4, on a spare, and re-dump. That is a read-after-change comparison on hardware the owner controls. This briefing does not describe how to flash a Smarty or an ECM.

## House rules

This is read-only documentation from two modules the owner already possessed. Do not treat it as a flash tutorial. Do not transmit the VP44 eleven-bit fueling IDs. Those frames are the ECM-to-pump conversation. Listen only.

Two physical boxes is also a practical fact. Keep a spare so a known factory still exists if something goes wrong with the truck that is in service. A twenty-five-year-old CM551 and a VP44 are easy to brick and out of scope here.

Read the maps. Same ROM, different fuel, identical timing, a truncated AFC asterisk, and two aftermarket products that do not contain these tables the way people hope they do. That is the show.
