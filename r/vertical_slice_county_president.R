# Phase 2 vertical slice #1: join county-level presidential results to
# county boundaries and plot a choropleth. County-level, not district-level,
# because that's the only results data downloaded so far (see
# docs/election-results-sources.md) — CD/SD/HD/Denver results are blocked.
#
# Usage: cd r && Rscript vertical_slice_county_president.R

library(sf)
library(arrow)
library(dplyr)
library(tidyr)
library(ggplot2)

source("load.R")

YEAR <- 2016

counties <- load_boundary("counties", "2024")

results <- read_parquet(file.path(DATA_ROOT, "processed", "election_results",
                                    "president_county", "2000-2016", "results.parquet"))

message(sprintf("\nLoaded %d result rows, years: %s",
                 nrow(results), paste(sort(unique(results$year)), collapse = ", ")))

year_results <- results %>%
  filter(year == YEAR, party %in% c("democrat", "republican")) %>%
  select(geoid, county_name, party, candidatevotes, totalvotes) %>%
  pivot_wider(names_from = party, values_from = candidatevotes) %>%
  mutate(
    dem_share = democrat / totalvotes,
    rep_share = republican / totalvotes,
    margin = dem_share - rep_share,  # positive = more Democratic
    winner = ifelse(margin > 0, "Democrat", "Republican")
  )

# Sanity check against the known statewide 2016 result (Clinton won CO by
# ~4.9 points) before trusting the per-county map.
statewide_dem <- sum(year_results$democrat)
statewide_rep <- sum(year_results$republican)
statewide_total <- sum(year_results$totalvotes)
statewide_margin <- (statewide_dem - statewide_rep) / statewide_total
message(sprintf(
  "\nStatewide %d: Dem %.2f%%, Rep %.2f%%, margin %.2f pts (expect ~Dem +4.9)",
  YEAR, 100 * statewide_dem / statewide_total, 100 * statewide_rep / statewide_total,
  100 * statewide_margin
))

joined <- counties %>%
  left_join(year_results, by = c("GEOID" = "geoid"))

n_missing <- sum(is.na(joined$margin))
message(sprintf("Counties with no matched result: %d (expect 0)", n_missing))

p <- ggplot(joined) +
  geom_sf(aes(fill = margin), color = "white", linewidth = 0.2) +
  scale_fill_gradient2(
    low = "firebrick", mid = "white", high = "steelblue", midpoint = 0,
    labels = scales::percent, name = "Dem margin"
  ) +
  labs(
    title = sprintf("Colorado %d Presidential Election — County Results", YEAR),
    subtitle = "County-level vertical slice (Phase 2) — results × boundaries"
  ) +
  theme_minimal()

dir.create("output", showWarnings = FALSE)
out_path <- file.path("output", sprintf("president_county_%d_choropleth.png", YEAR))
ggsave(out_path, p, width = 8, height = 6.5, dpi = 120)
message(sprintf("\nWrote %s", out_path))
