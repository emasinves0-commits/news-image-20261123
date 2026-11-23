# BUILD REPORT — news-image-20261123 ("The Monday Ledger")

- **Bounty:** news-image-20261123 ($100, 50 places), deadline 25 Nov 2026 00:00 UTC
- **Built:** 23 Nov 2026, ~01:40–02:12 UTC
- **Builder:** Muse subagent (session `34209fa5-6a27-4ec6-8e10-434d9ce567eb`). No Hermes/Claude Code session was used — the poster was built directly as deterministic Python/PIL code by this subagent (Claude Code is on its weekly limit until 24 Nov 03:00 UTC, per the brief).
- **Fix round:** 23 Nov 2026, ~02:15–02:20 UTC, by Muse subagent (session `e12019c5-9ac7-442b-8140-d16b7104e7a1`) — see "Fix round" below. New entry sha256 `29b3d59648952a555dbb7cde3274827e0bb27e9cdce3025e0be255131ffe250b`.
- **Base:** R5 `draw.py` geometry (~/workspace/makefun/news-image-20261121/draw.py) + the 6-cue checklist, rebuilt from scratch for the 23 Nov 2026 news day. The R5 story set was NOT reused — all 43 stories are fresh, full-day 23 Nov 2026.
- **Work dir:** ~/workspace/makefun/news-image-20261123/ — `draw.py` (the single source of truth; story data + all art + layout in one file), `entry.png`, `BUILD-REPORT.md` (this file), `crop_*.png` (eye-check crops).

## Entry

- **File:** `entry.png` — 1024×1024, RGB, **233,108 bytes** (after fix round; was 233,396)
- **SHA-256:** `29b3d59648952a555dbb7cde3274827e0bb27e9cdce3025e0be255131ffe250b`
- **Determinism:** three independent renders (working dir + two scratch dirs) are **byte-identical** (same sha256) for the original build; the fix-round re-render was also run twice with **byte-identical** output (same new sha256). No timestamps, no randomness in the render path.
- **Renderer warnings:** **zero** on the final render (no text overflow, no truncation, no shrink-to-fit below 9px in the ALSO list) — also zero after the fix round.

## Story set — 43 stories, 6 regions (asserted in code)

| Region | Count | Stories |
|---|---|---|
| EUROPE | 9 | 2 Antalya climate, 4 Gulf of Finland ship, 6 Kyiv drone, 14 Lisbon march, 23 Dnipropetrovsk strikes, 24 Poland/Russia rapper plot, 25 EU budget, 26 US intel chief on Putin, 27 May/Burnham Brexit |
| MIDDLE EAST | 8 | 1 Bahrain/US radars, 16 Houthi missile, 17 Hormuz tankers, 18 Iran Strait/uranium, 19 Pakistan FM, 20 Eisenkot settler attacks, 21 Netanyahu–Eisenkot talks, 22 Briton swims Hormuz |
| AMERICAS | 9 | 3 Democrats 258 seats, 8 Olympia ICE, 10 FBI crime-db hack, 13 Vegas GP, 28 Delta Atlanta, 29 Miley Cyrus wedding, 30 Tom Jackson dies, 31 Nvidia/China, 32 Alice Huang chip diversion |
| ASIA-PACIFIC | 11 | 7 Cikande factory fire, 9 Seoul AI cheating, 11 Nepal PM Delhi, 33 Amit Shah Arunachal, 34 IFFI BRICS, 35 MP Wadkute dies, 36 Kota bus crash, 37 Anupama snooker, 38 Hyderabad protest, 39 Japan markets shut, 40 Australia PMIs |
| AFRICA | 4 | 5 Libya port, 15 Juba SPLA-IO attack, 41 WHO Congo Ebola, 42 Sudan RSF killings |
| OCEANIA | 2 | 12 India 720/9 in NZ, 43 NZ Q3 retail sales (FORECAST) |

- **Leads (3):** 1 Bahrain/US radars (CLAIM vs DENIAL), 2 Antalya climate collapse (REPORTED), 3 Democrats 258 seats (REPORTED).
- **Small panels (12):** 4–15 as listed above, each with its own art function.
- **ALSO list (28):** stories 16–43, one line each, 3 columns, region-coloured number chips, source in parentheses.
- **Data strip (6 numbers):** 258 House seats · 0 'fossil fuels' mentions · 2 US radars claimed hit · 720/9 India Test total · 36 Cikande missing · 24 South Sudan dead.
- **UTC strip (5 beats):** Overnight Kyiv drone · Morning Cikande search resumes · Midday Nepal PM–Modi · Afternoon India 720/9 · Evening Antalya collapse.

## 6-cue checklist

1. **Data strip** — yes, 6 numbers with labels under the masthead.
2. **Pinned map** — yes: world map + EUROPE inset + MIDDLE EAST inset, 15 pins (one per panelled story, lat/lon placed), deterministic repulsion so pins never overlap, leader line + dot marks the true spot when a pin is displaced. Legend: pin colour = region.
3. **DATE CHECK box** — yes, red box: 5 excluded items named with their real dates (El Chapo Isidro Fri 20 Nov; Hong Kong Election Committee Sun 22 Nov; 186 drones over Ukraine Sat 22 Nov; Liverpool–Man Utd Sun 22 Nov; COP31 talks run into overtime Sat 22 Nov) + the line "Nothing here is dated to any day but Monday 23 November 2026, except the items named above as excluded."
4. **Region counts** — yes, full-width bar: EUROPE 10 · MIDDLE EAST 8 · AMERICAS 9 · ASIA-PACIFIC 11 · AFRICA 3 · OCEANIA 2 (code-asserted to sum to 43).
5. **Briefs** — yes: every panel has a 1–4-line body with a wire source; ALSO list carries sources.
6. **Illustrated panels** — yes: 15 distinct art functions, all original code-drawn (no photos, no reused graphics).

## R5 defect fixes — verified, not just claimed

- **Each panel its own art:** all 15 panels call a different art function (`bahrain`, `cop`, `house`, `ship_finland`, `libya`, `kyiv`, `factory`, `airport`, `seoul`, `cyber`, `delhi`, `cricket`, `f1`, `lisbon`, `juba`). Eye-checked every panel at full resolution — no art is reused, and no sub-label from one panel appears in another (the R5 "GULF OF FINLAND" label now belongs only to panel 4, its own ship art).
- **Region-bar names in full:** eye-checked the region bar at full resolution — "EUROPE 10", "MIDDLE EAST 8", "AMERICAS 9", "ASIA-PACIFIC 11", "AFRICA 3", "OCEANIA 2", all complete, no truncation.

## Eye-check — two rounds (all crops in this dir as `crop_*.png`)

**Round 1 (sha e67d6714…):** read the full poster + 6 section crops (top, leads, smalls ×2, map, bottom) at full resolution. Found and fixed:
1. Small panels overflowed their boxes by 7px (body ran past the panel bottom) — fixed by tightening small-panel geometry (art 30→28px, headline lh 13→12, body lh 12→11) and shortening 3 bodies.
2. Lead bodies 1 and 3 exceeded 3 lines — fixed by allowing 4 body lines in leads (panel 172→184px, map 128→116px to keep the 1024 budget) and shortening both bodies.
3. 20 ALSO items shrank to 8px — fixed by shortening those headlines/sources; 8 more shrank in the next pass and were shortened again.
4. Several small-panel art functions spilled above/below their 28px art box at small height (Delhi arch doorway inverted → crash; ship containers, Libya mast, cyber magnifier handle, cricket bat handle, F1 cockpit/flag pole, Lisbon placard pole, Juba canopy) — fixed each to stay inside the box at h=28. The Delhi crash was caught by the renderer (ValueError), the rest by auditing coordinates against the box.

**Round 2 (sha 60e55d8f…, final):** re-read the full poster + section crops + 3 targeted crops (lead 3 art, lead 2 art, panel 15) at 2–3× magnification. Found and fixed:
5. Lead 3 (Capitol) "258" label was white on the light-grey strip above the blue seat bar — nearly invisible. Moved it inside the blue bar (white on blue, high contrast). Verified in `crop_lead3art2.png`.
6. Lead 2 (Antalya) art had no place label (unlike the other leads). Added "ANTALYA" bottom-left on the table strip. Verified in `crop_lead2art2.png`.
7. Panel 15 body repeated its headline ("SPLA-IO attack in S. Sudan; 24 civilians dead"). Rewrote to add new information: "SPLA-IO attack; 24 dead, incl. 3 children. (Wires)". Verified in `crop_p15.png`.

**Round 2 re-check after fixes:** zero renderer warnings; panel slack 24/36/8 (leads) and 1px (all smalls — fits); all 15 art panels distinct; region bar full; map pins present and correctly placed (verified against lat/lon: 3+10 both Washington DC, spread apart with leader lines; 4 Gulf of Finland, 6 Kyiv, 14 Lisbon, 2 Antalya in the Europe inset; 1 Bahrain on the Gulf in the Middle East inset).

## Known nits (not defects — do not block)

- **Middle East inset is sparse:** only pin 1 (Bahrain) falls inside the ME box; pin 5 (Libya, lon 13.2) falls outside it and appears only on the world map. The inset is accurate but mostly empty beige. Filling it would mean pinning ALSO-list ME stories (16–22) on the map too, which would crowd the Gulf cluster on the small world map — judged not worth the clutter.
- **Map is pale:** light-tan land on light-blue sea is low-contrast at a glance, though the pins (coloured, white-outlined) read clearly. A stronger land/sea contrast would help the map pop.
- **Lead 1 art is dark/abstract:** the Bahrain night scene (dark sky, missile streak, "US 5th" box) reads as a strike, but the island + industrial buildings are small. Acceptable, not misleading.
- **Panel 8 body** ("Washington governor after two arrested at airport") is terse; the fuller context is in the headline ("Governor: ICE 'out of control'"). Fine as a brief.

## Fact notes for the parent's verification

- Story 5 (Libya port) is counted as AFRICA: Libya is in Africa; the panel place line says "LIBYA · DRONES" (geography). It was EUROPE in the first build (a Russia–Ukraine war-story grouping); the fix round moved it to AFRICA on the parent's eye-check, so the counts are now EUROPE 9, AFRICA 4 (total still 43).
- Story 26 (US intelligence chief: Putin 'not America's friend in Ukraine') is counted as EUROPE (Ukraine subject); story 31/32 (Nvidia/China chip rows) as AMERICAS (US policy subject). Both are judgement calls, documented here.
- "258 seats … largest majority since 1992" is the wire figure as reported on 23 Nov 2026 (Democrats' 258th seat, Chuck Hubbard beating Rep. Virginia Foxx in North Carolina; 44 seats gained; four races uncalled at the time of drawing).
- The "720/9" cricket score, "1:37.924" pole time, and "24 body bags found" at Cikande are as reported in the 23 Nov wires; the Cikande body says "24 bags found" (shortened from "24 body bags found Sunday" to fit two lines — the "Sunday" is dropped, the count is kept).

## Fix round (23 Nov 2026, ~02:15–02:20 UTC — subagent `e12019c5`)

The parent eye-checked `entry.png` + crops and sent 4 defects. The fix subagent
verified each against the pixels before changing anything:

1. **Alleged defect — Tom Jackson labelled MIDDLE EAST at item 20: DOES NOT EXIST.** The fix subagent read `crop_bottom.png` AND a fresh 2× magnified crop cut directly from `entry.png`: item 20 is "Eisenkot: settler attacks are 'Jewish terrorism'" (MIDDLE EAST — correct), and Tom Jackson is item 30, labelled **AMERICAS** (correct) in both the old and new renders. The parent's reading conflated row 5 across the ALSO columns (item 20 in column 1 vs item 30 in column 2). No change made; the counts stay MIDDLE EAST 8 / AMERICAS 9. **The parent's combined count change (ME 7 / AMERICAS 10) was NOT applied — it would have made the counts wrong.**
2. **DATE CHECK false claim — FIXED.** "COP31 final text agreed (Sat 22 Nov)" was factually wrong: COP31 collapsed Sunday with no agreement (Reuters/CNN/BBC/Le Monde). Reworded to the true excluded item "COP31 talks run into overtime (Sat 22 Nov)". Verified in `crop_fix_bottom.png`.
3. **Libya counted as EUROPE — FIXED.** Story 5 (Libya port) moved to AFRICA (geography: Libya is in Africa). `REGION_OF[5] = "AFRICA"`; assert + comment updated. Region bar now reads EUROPE 9, AFRICA 4 (total still 43). Verified in `crop_fix_top.png`; the Libya map pin (13.2, 32.9) changed from blue to green automatically.
4. **Panel 8 body garbled — FIXED.** "Washington governor after two arrested at airport." → "Washington governor speaks after airport arrests. (Wires)" (59 chars, fits in 2 lines, slack 1px, zero renderer warnings). Verified in `crop_fix_p8full.png`.

**Fix-round re-verification:** two renders byte-identical (sha256 `29b3d596…`), zero renderer warnings, panel slack unchanged (leads 24/36/8, smalls 1px), no new overlaps (full bottom crop re-read). Fix crops in this dir: `crop_fix_top.png`, `crop_fix_p8.png`, `crop_fix_p8full.png`, `crop_fix_bottom.png`.

## What the parent still needs to do

- Eye-check `entry.png` (this report's crops are a starting point, not a substitute).
- Vote (all subordinates), bundle, submit. Repo: emasinves0-commits/news-image-20261123 — **files pushed 23 Nov 02:2x UTC by the fix subagent (draw.py, entry.png, README.md, main.ts, LICENSE, BUILD-REPORT.md, .makefun/owner.json); remote HEAD `TBD`**.
- Send `entry.png` to Mhmd with the submit confirmation (standing news-image rule).
