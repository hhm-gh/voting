# Redistricting & Gerrymandering — Colorado

Deep dive on how Colorado draws its congressional and state legislative
districts, and on the general vocabulary/metrics used to detect
gerrymandering. Builds on [`geography.md`](geography.md), which covers what
a Congressional/State Senate/State House district *is*; this doc covers how
their boundaries get drawn and how to judge whether a map is fair.

Denver City Council redistricting is **not** covered by the mechanism below —
council districts are redrawn through Denver's own charter process, not the
state commissions. That process still needs its own research pass (flagged
as an open question in `geography.md`).

This doc also covers the national mid-decade redistricting fight that broke
out in 2025–2026 (see [National Context](#national-context-20252026-the-mid-decade-redistricting-wave)
below) — it's directly relevant background, since Colorado's own commission
was pulled into that fight in 2026, and it's fast-moving enough that this
section should be treated as a snapshot, not a settled record.

## Background: why Colorado changed its process

Historically, Colorado's congressional map was drawn by the state
legislature (subject to governor veto and courts as tiebreaker) and its
legislative maps by a commission dominated by legislative and party
appointees. In **2018**, Colorado voters passed two constitutional
amendments to replace both processes with independent commissions:

- **Amendment Y** — Independent Commission for **Congressional** Redistricting
- **Amendment Z** — Independent Commission for **State Legislative**
  Redistricting (state Senate + House)

Both passed with large majorities and created near-identical
processes/criteria, just for different maps. They first applied to the maps
drawn after the **2020 Census**, used starting with the 2022 elections, and
will apply again after the **2030 Census**.

## Commission structure

Each commission (congressional and legislative are separate 12-member
bodies) is composed of:

- **4 members** affiliated with the state's largest political party (Democratic)
- **4 members** affiliated with the state's second-largest political party (Republican)
- **4 members** unaffiliated with any political party

### How members are chosen
1. Colorado opens a public application process; a nonpartisan legislative
   staff panel screens applicants for basic qualifications.
2. From the qualified pool, a **panel of three retired Colorado appellate
   judges** (appointed by the Chief Justice, deliberately of mixed party
   background) narrows candidates to pools of 50 Democrats, 50 Republicans,
   and 50 unaffiliated applicants per commission.
3. Legislative leaders (majority/minority leaders of the state House and
   Senate) can each strike a limited number of names from the pools.
4. The judicial panel randomly selects some commissioners directly from the
   pools, and selects the remaining commissioners from narrower lists,
   balancing party affiliation, so each commission ends up with its 4/4/4 split.

This design (random selection + retired-judge oversight + capped legislative
input) is the core "independence" mechanism — no sitting legislator, the
governor, or party leadership directly appoints commissioners.

## How a map gets approved

- A map needs a **supermajority of 8 of the 12 commissioners**, which must
  include **at least 2 of the 4 unaffiliated members**. This is the key
  structural safeguard: neither major party's 4 members, even combined with
  friendly unaffiliated votes, can approve a map without support that
  crosses the partisan lines within the unaffiliated bloc.
- If the commission cannot reach 8 votes (including 2 unaffiliated) by its
  statutory deadline, a **nonpartisan legislative staff plan** is submitted
  to the Colorado Supreme Court by default instead.
- Either way, the **Colorado Supreme Court must approve the final plan**
  before it takes effect, reviewing it against the constitutional criteria
  below. This happened in practice in 2021: the congressional map passed the
  commission 11–1 and was unanimously approved by the Court on 2021-11-01;
  the legislative (Senate/House) maps were approved by the Court on
  2021-11-15.

## Map-drawing criteria (in priority order)

The amendments specify criteria the commissions must apply, in a strict
priority order — each criterion only breaks ties left by the one above it:

1. **Federal constitutional/legal compliance** — equal population (a
   good-faith effort at precise mathematical population equality between
   districts, justifying every deviation, however small) and compliance
   with the Voting Rights Act (no denial/abridgment of minority voting
   rights; where possible, preserve minority communities' ability to elect
   their preferred candidates).
2. **Preserve whole communities of interest and whole political
   subdivisions** (counties, cities, towns) as much as reasonably possible
   — i.e., avoid splitting a county or town across multiple districts
   unless population equality forces it.
3. **Compactness** — districts must be as geographically compact as is
   reasonably possible (see compactness metrics below).
4. **Competitiveness** — only after the above are satisfied, the commission
   shall, to the extent possible, maximize the number of politically
   competitive districts.

Critically, the amendments **explicitly prohibit** drawing maps for the
purpose of protecting or favoring any incumbent, declared candidate, or
political party — the opposite priority ordering from what enables
gerrymandering in states without this kind of reform.

## Gerrymandering vocabulary & metrics

These are the general-purpose tools used (in academic and legal contexts) to
detect and quantify gerrymandering. Useful vocabulary for Phase 4 of the
[overview plan](../OVERVIEW.md#phase-4--analysis--visualization) once we
have real district + result data to apply them to.

**Note on data granularity:** every metric below requires **precinct-level**
(or block-level) results, not just district totals — district totals are
the thing being evaluated, so there's nothing smaller to reshuffle when
testing against alternative maps. This is why precinct acquisition is
deferred to Phase 3/4 rather than pulled in during Phase 1; see
[`data-sources.md`'s precinct section](data-sources.md#precincts-deferred--phase-34-not-phase-1)
for the full reasoning and sourcing options.

- **Packing** — concentrating one party's voters into a small number of
  districts they win by huge margins, "wasting" their surplus votes.
- **Cracking** — spreading one party's voters thinly across many districts
  so they fall short of a majority in each.
- **Wasted votes** — for a given party, all votes cast for losing
  candidates, plus all votes cast for winning candidates beyond the minimum
  needed to win (i.e., surplus). Packing and cracking both work by
  engineering wasted votes for the opposing side.
- **Efficiency gap** — (party A's wasted votes − party B's wasted votes) /
  total votes cast, statewide. Captures net packing+cracking in one number;
  a large efficiency gap in one party's favor is a common (though
  contested) statistical signal of partisan gerrymandering.
- **Partisan symmetry / mean-median score** — asks whether the map would
  treat the two parties symmetrically if their vote shares were swapped;
  the mean-median score specifically measures how far a party is from
  winning half the seats after winning half the statewide vote.
- **Compactness scores** — geometric measures of district shape, since
  bizarrely shaped districts are a visual (if imperfect) gerrymandering
  signal. Two common formulas:
  - **Polsby-Popper**: 4π × (area / perimeter²) — penalizes long, winding
    perimeters.
  - **Reock**: district area / area of the smallest enclosing circle —
    penalizes elongated or sprawling shapes.
  Compactness metrics are useful but gameable — a map can score well on one
  compactness formula while still being an effective partisan gerrymander,
  so they're best used alongside efficiency gap / symmetry metrics, not
  alone.

None of these metrics is universally agreed to be "the" correct test for
gerrymandering (including in case law — the U.S. Supreme Court has declined
to adopt a single standard); treat them as complementary lenses rather than
a pass/fail formula.

## National context (2025–2026): the mid-decade redistricting wave

Normally, congressional and legislative maps are redrawn once per decade,
right after the Census. Starting in **July 2025**, that norm broke down:
President Trump directly urged Texas Republicans to redraw the state's
congressional map *mid-decade* to manufacture additional GOP-leaning seats
ahead of the **2026 midterms**, given Republicans' narrow US House majority.
That triggered what trackers (Ballotpedia, Democracy Docket, NCSL) describe
as the largest coordinated mid-decade redistricting effort in modern US
history — a partisan "arms race" that, as of mid-2026, is still unfolding.

**The office at stake is almost exclusively the US House.** Unlike the
Colorado-specific material above, this wave has barely touched state
legislative maps, and by definition can't touch the US Senate (Senate seats
aren't districted). Control of the US House majority for the second half of
Trump's term is the immediate stake, which is why this is a Congressional-
district story first and foremost — worth keeping in mind when scoping which
races this project treats as "live" gerrymandering-risk vs. mostly settled
(state legislative maps, city council maps).

### State-by-state, in brief (snapshot as of mid-2026 — check live trackers for current status)

- **Republican-favoring maps adopted**: Texas, North Carolina, Missouri,
  Ohio, Florida, Tennessee, Alabama, Louisiana. (Ohio is a partial exception:
  its redraw was constitutionally *required* because the prior map never got
  bipartisan support, but the commission used the opportunity to shift the
  delegation from a 10R–5D to a 12R–3D lean.)
- **Republican-led legislature that rejected a redraw**: **Indiana** —
  Governor Braun called a special session at Trump's request, but the state
  Senate voted 31–19 against the new map on 2025-12-11 (21 Republicans
  joined all 10 Democrats). Because it lost by a constitutional majority,
  it can't be brought back up until the 2027 session — the first instance of
  a GOP legislature publicly defying this push.
- **Democratic countermove**: **California** — voters approved
  **Proposition 50** (Nov. 2025, backed by Gov. Newsom), a ballot measure
  establishing a new, Democratic-favoring congressional map for the 2026,
  2028, and 2030 elections, explicitly framed as a response to Texas.
- **Court-driven change**: **Utah** — courts ordered a new map ending an
  existing GOP gerrymander (tied to Utah's own 2018 independent-redistricting
  ballot initiative litigation), producing a Democratic-favoring result
  without a legislative vote.
- **Struck down**: **Virginia** — a Democratic-backed redistricting
  referendum was invalidated by the Virginia Supreme Court (May 2026).
- Several states (Maryland, Florida's later moves, Washington) were still
  "navigating" redraw efforts as of early 2026 per trackers — treat the list
  above as a snapshot, not final.

Trackers generally describe the net national effect so far as favoring
Republicans (more GOP-led states completed maps, and completed them
successfully, compared to Democratic-led counter-efforts) — but exact
seat-swing counts vary by source and are still moving; don't treat any
specific number as settled without checking a live tracker.

### The legal backdrop: *Louisiana v. Callais* and the Voting Rights Act

On **2026-04-29**, the US Supreme Court ruled 6–3 in *Louisiana v. Callais*
(consolidated with *Robinson v. Callais*), striking down a Louisiana
congressional map that had created a second majority-Black district to
comply with Section 2 of the Voting Rights Act — holding that drawing a
district to satisfy Section 2 was itself an unconstitutional racial
gerrymander. Coverage from the Brennan Center and Campaign Legal Center
describes this as substantially narrowing Section 2 going forward:
challengers must now show a map was drawn *because of* race (not just that
it has a race-correlated effect) and must show current, intentional
discrimination rather than statistical vote dilution. Practical effect:
several states are moving to eliminate or reconfigure existing
majority-minority districts for 2026, since the main legal tool historically
used to require or defend them is now weaker. This bears directly on the
**packing/cracking** vocabulary above — VRA Section 2 was one of the few
tools available specifically to challenge packing/cracking of racial
minority voters, and that tool just got smaller.

Relatedly, in Texas a federal district court found the 2025 map to be a
racial gerrymander (Nov. 2025), but the Supreme Court stayed that ruling
(Dec. 2025) and then, in an April 27 2026 order (just before *Callais*),
let the map stand 6–3 through at least 2030 — a preview of the direction
*Callais* would confirm days later.

### Colorado specifically

Colorado's independent commissions (Amendments Y & Z) explicitly forbid
partisan map-drawing, and the state's next scheduled full redraw isn't until
after the 2030 Census — but Colorado was pulled directly into this fight
anyway in 2026:

- A Democratic-aligned group, **Coloradans for a Level Playing Field**,
  filed three ballot measures for the Nov. 2026 ballot that would have
  temporarily paused the independent congressional commission so voters
  could approve a new map — reportedly one that could have flipped as many
  as 7 of Colorado's 8 US House seats to Democrats, leaving only 1
  Republican-held seat.
- Republicans filed counter-measures that would have required Colorado
  Supreme Court and commission review of any map drawn outside the
  independent process.
- On **2026-06-29**, the Colorado Supreme Court rejected the Democratic-
  backed measures — but on narrow technical grounds (the state
  constitution's single-subject and clear-title requirements for ballot
  initiatives), not on the merits of pausing the commission. Colorado's
  independent commission remains intact and unmodified for 2026, but this
  doesn't foreclose a more carefully drafted measure in the future.
- A separate proposal for a constitutional amendment granting "emergency
  redistricting authority" ahead of **2028** has reportedly been floated —
  worth tracking as an open, unresolved thread rather than settled.

This is a live stress test of the exact design described earlier in this
doc (supermajority + unaffiliated-bloc requirement, no-partisan-favor rule):
Colorado is one of the few states whose entire *anti*-gerrymandering model
is currently being tested by the same national forces driving gerrymandering
elsewhere.

## Open questions / things to verify later

- Exact statutory deadlines each commission had for its cycle (useful for
  building a timeline visualization of the 2021 process).
- The precise population-deviation tolerance actually used for the state
  House/Senate maps (congressional districts require near-exact equality;
  legislative maps are typically allowed a small percentage deviation to
  accommodate the other criteria — needs a citation before treating as fact).
- Denver City Council's own redistricting process/criteria (charter-based,
  separate from Amendment Y/Z) — still unresearched.
- Whether Colorado's 2021 maps have been legally challenged since adoption
  on population/VRA grounds specifically (distinct from the 2026 ballot-
  measure fight over *pausing* the commission, covered above), as a
  real-world case study for the metrics above.
- Whether the "emergency redistricting authority for 2028" proposal
  mentioned above advances, and what it would actually change if adopted.
- A running seat-swing tally for the 2025–2026 national wave, once trackers
  settle — current numbers vary by source and shouldn't be treated as fixed.

## Related docs

- [`geography.md`](geography.md) — what each district type is and how
  precincts aggregate into them
- [`../OVERVIEW.md`](../OVERVIEW.md) — project goals and phased plan
- `offices.md` (planned) — office-by-office catalog

## Sources

- [Colorado Independent Redistricting Commissions (official site)](https://redistricting.colorado.gov/)
- [Ballotpedia: Colorado Amendment Y (2018)](https://ballotpedia.org/Colorado_Amendment_Y,_Independent_Commission_for_Congressional_Redistricting_Amendment_(2018))
- [Ballotpedia: Colorado Amendment Z (2018)](https://ballotpedia.org/Colorado_Amendment_Z,_Independent_Commission_for_State_Legislative_Redistricting_Amendment_(2018))
- [Colorado Sun: Supreme Court approves new congressional map (2021-11-01)](https://coloradosun.com/2021/11/01/colorado-congressional-map-approved-supreme-court/)
- [Colorado Sun: legislative maps get final court approval (2021-11-15)](https://coloradosun.com/2021/11/15/colorado-redistricting-legislative-maps-court-approval/)
- [Colorado Newsline: commission member selection process](https://coloradonewsline.com/briefs/final-six-members-of-colorados-new-congressional-redistricting-commission-selected/)
- [Harvard Law School bibliography: Partisan Gerrymandering and the Efficiency Gap (Stephanopoulos & McGhee)](https://hls.harvard.edu/bibliography/partisan-gerrymandering-and-the-efficiency-gap/)

**National context (2025–2026 redistricting wave):**

- [Wikipedia: 2025–2026 United States redistricting](https://en.wikipedia.org/wiki/2025%E2%80%932026_United_States_redistricting)
- [Ballotpedia: Redistricting ahead of the 2026 elections](https://ballotpedia.org/Redistricting_ahead_of_the_2026_elections)
- [Democracy Docket: Live Redistricting Tracker](https://www.democracydocket.com/analysis/live-redistricting-tracker/)
- [NCSL: Changing the Maps — Tracking Mid-Decade Redistricting](https://www.ncsl.org/redistricting-and-census/changing-the-maps-tracking-mid-decade-redistricting)
- [NPR: In a setback for Trump, Indiana lawmakers defeat redistricting plan (2025-12-11)](https://www.npr.org/2025/12/11/nx-s1-5637488/midterm-elections-trump-redistricting-indiana)
- [SCOTUSblog: Supreme Court strikes down Louisiana map in *Louisiana v. Callais* (2026-04-29)](https://www.scotusblog.com/2026/04/in-major-voting-rights-act-case-supreme-court-strikes-down-redistricting-map-challenged-as-racia/)
- [Campaign Legal Center: The Supreme Court Has Eviscerated the Voting Rights Act — What's Next?](https://campaignlegal.org/update/us-supreme-court-has-eviscerated-voting-rights-act-whats-next)
- [Colorado Sun: Supreme Court rejects Democrat redistricting ballot initiative (2026-06-29)](https://coloradosun.com/2026/06/29/colorado-supreme-court-rejects-democrat-redistricting-plan-initiative-240/)
- [Colorado Politics: National redistricting fight reaches Colorado (2026-02-18)](https://www.coloradopolitics.com/2026/02/18/national-redistricting-fight-reaches-colorado-with-ballot-measures-targeting-gop-held-congressional-districts/)
