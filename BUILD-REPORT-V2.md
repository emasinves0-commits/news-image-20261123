# BUILD REPORT — news-image-20261123 v2 ("The Monday Ledger", legibility-first redesign)

- **Bounty:** news-image-20261123 ($100, 50 places), deadline 25 Nov 2026 00:00 UTC
- **Built:** 24 Nov 2026, ~14:05–14:25 UTC
- **Builder:** Muse subagent (session `03221432-3d66-461e-a432-306f32a9474e`) — NOT Claude Code.
  **Why:** Claude Code was ordered for this poster, but its login is broken on this VM
  right now: `claude -p` exits with "Not logged in · Please run /login" (verified
  14:00 UTC, twice), no OAuth token exists anywhere (`~/.claude/.credentials.json`
  missing, no oauth in `~/.claude.json`). A sibling session worked 13:44–13:49 UTC
  today, another failed auth 13:59 UTC — the login broke between those times.
  Re-login needs Mhmd in a browser and cannot be done from here. Fallback follows
  the v1 precedent: v1 was also built directly by a Muse subagent (Claude Code was
  on its weekly limit then) and was submitted and scored. The parent should re-login
  Claude Code when possible; this v2 is ready to submit as built.
- **Base:** v1 `draw.py` + `BUILD-REPORT.md` (43 verified 23-Nov stories, fixed defects).
  All 31 v2 stories are a subset of v1's verified set — no new facts invented.
- **Work dir:** ~/workspace/makefun/news-image-20261123/ — `draw_v2.py` (new file;
  `draw.py` kept untouched as the v1 record), `entry_v2.png`, `BUILD-REPORT-V2.md`
  (this file), `crop_v2_*.png` (eye-check crops).

## Diagnosis (why v1 lost, what v2 changes)

- v1 round 2: rank **1091/9643, 64.08%**. Prize line = final top 52 (playoff).
  Leaders score ~85% (bagarte won news-22 at 85.44%).
- Leader pattern (bagarte news-22 top 1, superskie news-21 top 1 — both read from
  their images): 35–37 stories, 13 panels (3 huge leads + 10 smalls), big red
  banner headlines on the leads, 6-number "day in numbers" strip, one world map
  with numbered pins, DATE CHECK box, UTC timeline, sources beside every story.
- v1's weaknesses vs that pattern: 43 stories (over-dense); 12 small panels in
  2×6 with 28px art and 3-line 11px bodies; lead art small and (lead 1) dark and
  abstract; map pale with tiny unnumbered pins; data numerals small; and at the
  ~300px width the poster is judged at, everything below the leads dissolved
  into unreadable grey — the judge's criterion 5 (legible at ~300px) and
  criterion 3 (it reads) both suffer, and the judge says "detail for its own
  sake does not count".
- **New gap (the point of v2): legibility-first.** No leader closes it — their
  ALSO lists are also ~8px text. v2 has NO text below 10px anywhere, headlines
  12–15px, bodies 11px, lead banner headlines readable at thumbnail size, map
  pins 16px with 10px numbers, 31 stories instead of 43. Verified at 300px wide:
  masthead date, three lead banners, six data numbers and the pinned map all
  still read (see `crop_v2_300px.png`).
- Combined: winners' structure (3 huge leads + 10 smalls + day-in-numbers + map
  + date check + UTC strip) + legibility-first (fewer stories, bigger everything).

## Entry

- **File:** `entry_v2.png` — 1024×1024, RGB, **228,511 bytes**
- **SHA-256:** `7a096e8e45994db8c00d7817915570b481c6fb6b60c8682429f1c49b70aacf18`
- **Determinism:** three independent renders are **byte-identical** (same sha256).
  No timestamps, no randomness in the render path.
- **Renderer warnings:** **zero** on the final render (no overflow, no truncation,
  no text below the 10px floor — the floor is asserted in code).
- **Title for submit:** "Monday 23 November 2026 — 31 stories: COP31 collapses, the Gulf burns, Democrats take 258"
  (v1's title "Oceanic Gauge" did not name the day; leaders' titles do.)

## Story set — 31 stories, 6 regions (asserted in code)

| Region | Count | Stories |
|---|---|---|
| EUROPE | 8 | 2 Antalya climate, 4 Gulf of Finland ship, 6 Kyiv drone, 14 Lisbon march, 23 Dnipropetrovsk strikes, 24 Poland/Russia rapper plot, 25 EU budget, 26 US intel chief on Putin |
| MIDDLE EAST | 5 | 1 Bahrain/US radars, 16 Houthi missile, 17 Hormuz tankers, 18 Iran Strait/uranium, 20 Eisenkot settler attacks |
| AMERICAS | 6 | 3 Democrats 258 seats, 8 Olympia ICE, 10 FBI crime-db hack, 13 Vegas GP, 28 Delta Atlanta, 31 Nvidia/China |
| ASIA-PACIFIC | 7 | 7 Cikande factory fire, 9 Seoul AI cheating, 11 Nepal PM Delhi, 12 India 720/9, 33 Amit Shah Arunachal, 36 Kota bus crash, 38 Hyderabad protest |
| AFRICA | 4 | 5 Libya port, 15 Juba SPLA-IO attack, 41 WHO Congo Ebola, 42 Sudan RSF killings |
| OCEANIA | 1 | 43 NZ Q3 retail sales (FORECAST) |

- **Leads (3):** 1 Bahrain/US radars (CLAIM vs DENIAL), 2 Antalya climate collapse (REPORTED), 3 Democrats 258 seats (REPORTED). Bodies shortened from v1 without changing facts (lead 1 drops "violation of sovereignty", lead 3 drops nothing material).
- **Small panels (10):** 4, 6, 7, 8, 9, 11, 12, 13, 14, 15 — each with its own art function.
- **ALSO list (18):** 5, 10, 16, 17, 18, 20, 23, 24, 25, 26, 28, 31, 33, 36, 38, 41, 42, 43 — two columns, one line each at 11px, region-coloured number chips, source in parentheses.
- **Dropped vs v1 (12):** 19 Pakistan FM, 21 Netanyahu–Eisenkot, 22 Briton swims Hormuz, 27 May/Burnham, 29 Miley Cyrus wedding, 30 Tom Jackson dies, 32 Alice Huang, 34 IFFI BRICS, 35 Wadkute dies, 37 Anupama snooker, 39 Japan markets shut, 40 Australia PMIs — the softest / celebrity / forecast-adjacent items, to buy type size. All were verified 23-Nov stories; dropping them loses nothing the judge weighs (breadth kept: all 6 regions, politics/war/climate/sport/culture/economy).
- **Data strip (6 numbers):** same six as v1 — 258 House seats · 0 'fossil fuels' mentions · 2 US radars claimed hit · 720/9 India Test total · 36 Cikande missing · 24 South Sudan dead.
- **UTC strip (5 beats):** same as v1.
- **Map:** world map + EUROPE inset + MIDDLE EAST inset, **all 31 stories pinned** (v1 pinned only the 15 panelled stories) — this also cures v1's "Middle East inset sparse" nit (now 5 pins: 1, 16, 17, 18, 20). Higher contrast than v1 (darker land, deeper sea). Pins 16px with 10px white numbers, deterministic repulsion, leader line + dot marks the true spot when displaced.
- **DATE CHECK box:** same 5 verified excluded items as v1 (fix-round wording).

## 6-cue checklist

1. **Data strip** — yes, 6 numbers with labels under the masthead.
2. **Pinned map** — yes: world map + 2 insets, 31 pins (one per story), numbered.
3. **DATE CHECK box** — yes, red box with 5 excluded items + the "nothing here is dated to any other day" line.
4. **Region counts** — yes, full-width bar: EUROPE 8 · MIDDLE EAST 5 · AMERICAS 6 · ASIA-PACIFIC 7 · AFRICA 4 · OCEANIA 1 (code-asserted to sum to 31).
5. **Briefs** — yes: every panel has a 2–3-line body with a wire source; ALSO list carries sources.
6. **Illustrated panels** — yes: 13 distinct art functions, all original code-drawn.

## Eye-check — full read + 2 fix rounds (all crops in this dir as `crop_v2_*.png`)

**Round 1 (sha 6a8f80cc…):** read the full poster + 7 section crops (top, leads, smalls ×2, map 2×, ALSO, bottom) at full resolution. Found:
1. Lead 3 body overflowed its box by 1px — fixed by shrinking lead art 98→96px.
2. Footer sources line overflowed at the 10px floor — fixed by shortening the line (dropped "The" + "CERTAINTY: … labelled as such · still to happen when drawn" phrasing).
3. **OCEANIA blue ≈ EUROPE blue** — region colour collision (v1's too: (20,90,160) vs (30,78,160)). Fixed: OCEANIA is now orange (232,128,20) — distinct in the region bar, ALSO chips, map pins and legend.
4. Lead 3 Capitol dome read as a white blob — fixed: narrower dome + small red flag on the spire.
5. Seoul small-panel art sparse (mostly white sky) — noted, not a defect: desks + warning laptop read as an exam hall.

**Round 2 (sha 7a096e8e…, final):** re-read full poster + top + map 2× + lead 3 + 300px render. Verified:
- Region bar: all six names + counts complete, OCEANIA now orange.
- Map: all 31 pins present and numbered; Europe inset 2, 4, 6, 14, 23, 24, 25; ME inset 1, 16, 17, 18, 20; world map the rest; pin 4's leader line reaches its true spot at the inset's top edge.
- ALSO list: all 18 region labels match their stories (read each one).
- DATE CHECK + footer: both read clean at full resolution.
- **300px test:** masthead date, three lead banner headlines, six data numbers and the pinned map all still read at 300px wide (`crop_v2_300px.png`). Small-panel bodies and the ALSO list blur out at that size — as designed; they are detail, not the read.
- Zero renderer warnings; panel slack ≥1px everywhere (leads 17/17/1, smalls 3–16).

## Known nits (not defects — do not block)

- **Lead 1 art is still a night scene** (dark sky) — but now with a pale moon, lit skyline, island, fire burst and the "US 5th" box; reads clearly as a Gulf strike at full res and at 300px.
- **Americas pins cluster on the world map** (3, 10, 26, 31 all Washington DC + 8 Olympia + 13 Vegas + 28 Atlanta) — each pin is individually readable after repulsion; the cluster honestly shows how US-heavy the day's wire was.
- **Panel 7/9 art is simple** (flames, desks) — readable and distinct, not misleading.

## What the parent still needs to do

- Eye-check `entry_v2.png` (this report's crops are a starting point, not a substitute).
- Promote `entry_v2.png` → `entry.png` (local copy) and push: `draw_v2.py`, `README.md`, `BUILD-REPORT-V2.md` (text) + `entry.png` (binary) to repo `emasinves0-commits/news-image-20261123`; verify remote tree SHAs.
- Bundle + kit check + submit (parent's call). Bundle must include the v1 build sessions (their transcripts authored the reused lines) + this session (`03221432-3d66-461e-a432-306f32a9474e`).
- Suggested title: "Monday 23 November 2026 — 31 stories: COP31 collapses, the Gulf burns, Democrats take 258".
- Send `entry.png` to Mhmd with the submit confirmation (standing news-image rule).
- Re-login Claude Code when possible (see Builder note above) — the standing rule wants Claude Code for news-image posters; this v2 is the documented fallback, as v1 was.
