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

## Open questions / things to verify later

- Exact statutory deadlines each commission had for its cycle (useful for
  building a timeline visualization of the 2021 process).
- The precise population-deviation tolerance actually used for the state
  House/Senate maps (congressional districts require near-exact equality;
  legislative maps are typically allowed a small percentage deviation to
  accommodate the other criteria — needs a citation before treating as fact).
- Denver City Council's own redistricting process/criteria (charter-based,
  separate from Amendment Y/Z) — still unresearched.
- Whether Colorado's 2021 maps have been legally challenged since adoption,
  and on what grounds, as a real-world case study for the metrics above.

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
