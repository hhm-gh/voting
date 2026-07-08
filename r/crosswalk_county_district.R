# Phase 2 crosswalk task, county tier: does each Colorado county sit wholly
# inside one CD/SD/HD, or does it get split across multiple? Tests the
# "preserve whole counties" redistricting criterion (docs/redistricting.md)
# empirically, using boundaries already downloaded — no new data needed.
#
# Area-based, not just intersects(): two independently-sourced shapefiles
# (Colorado's redistricting commission vs. Census TIGER counties) will not
# share exact edges, so naive intersection would flag nearly every
# border county as "split" on sliver overlaps. A county only counts as
# genuinely split if a second district covers more than SLIVER_THRESHOLD
# of its area.
#
# Usage: cd r && Rscript crosswalk_county_district.R

library(sf)
library(dplyr)
library(ggplot2)

source("load.R")

SLIVER_THRESHOLD <- 0.01  # 1% of county area — below this, treat as topology noise
EQUAL_AREA_CRS <- 5070    # NAD83 / Conus Albers — appropriate for CONUS-scale area math

counties <- load_boundary("counties", "2024") %>%
  st_transform(EQUAL_AREA_CRS) %>%
  st_make_valid() %>%
  mutate(county_area = st_area(st_geometry(.)))

analyze_crosswalk <- function(district_name, district_cycle, district_id_col) {
  message(sprintf("\n=== %s vs counties ===", district_name))

  districts <- load_boundary(district_name, district_cycle) %>%
    st_transform(EQUAL_AREA_CRS) %>%
    st_make_valid()

  pieces <- st_intersection(
    counties %>% select(GEOID, NAME, county_area),
    districts %>% select(district_id = all_of(district_id_col))
  ) %>%
    mutate(piece_area = st_area(st_geometry(.))) %>%
    st_drop_geometry() %>%
    mutate(share_of_county = as.numeric(piece_area / county_area))

  meaningful <- pieces %>% filter(share_of_county >= SLIVER_THRESHOLD)

  per_county <- meaningful %>%
    group_by(GEOID, NAME) %>%
    summarise(
      n_districts = n_distinct(district_id),
      districts = paste(sort(unique(district_id)), collapse = ", "),
      .groups = "drop"
    )

  split_counties <- per_county %>% filter(n_districts > 1)

  message(sprintf(
    "%d of %d counties (%.0f%%) are split across >1 district (>%.0f%% of area threshold)",
    nrow(split_counties), nrow(per_county),
    100 * nrow(split_counties) / nrow(per_county), 100 * SLIVER_THRESHOLD
  ))

  if (nrow(split_counties) > 0) {
    for (i in seq_len(nrow(split_counties))) {
      row <- split_counties[i, ]
      detail <- meaningful %>%
        filter(GEOID == row$GEOID) %>%
        arrange(desc(share_of_county))
      shares <- sprintf("%s (%.0f%%)", detail$district_id, 100 * detail$share_of_county)
      message(sprintf("  %s: %s", row$NAME, paste(shares, collapse = ", ")))
    }
  }

  list(name = district_name, per_county = per_county, split_counties = split_counties)
}

cd_result <- analyze_crosswalk("congressional", "2021", "District")
sd_result <- analyze_crosswalk("state_senate", "2021", "District")
hd_result <- analyze_crosswalk("state_house", "2021", "District")

summary_df <- bind_rows(
  cd_result$per_county %>% mutate(geography = "congressional"),
  sd_result$per_county %>% mutate(geography = "state_senate"),
  hd_result$per_county %>% mutate(geography = "state_house")
)

dir.create("output", showWarnings = FALSE)
write.csv(summary_df, "output/county_district_crosswalk_summary.csv", row.names = FALSE)
message(sprintf("\nWrote output/county_district_crosswalk_summary.csv (%d rows)", nrow(summary_df)))

# Bonus visualization: highlight which counties are split for congressional
# districts specifically, since that's the most policy-salient tier.
plot_df <- counties %>%
  left_join(cd_result$per_county %>% select(GEOID, n_districts), by = "GEOID") %>%
  mutate(split = ifelse(n_districts > 1, "Split across multiple CDs", "Whole within one CD"))

p <- ggplot(plot_df) +
  geom_sf(aes(fill = split), color = "white", linewidth = 0.2) +
  scale_fill_manual(values = c("Split across multiple CDs" = "firebrick",
                                "Whole within one CD" = "grey85"), name = NULL) +
  labs(
    title = "Colorado Counties Split Across Congressional Districts (2021 map)",
    subtitle = sprintf("Area-based, >%.0f%% threshold — not just touching edges", 100 * SLIVER_THRESHOLD)
  ) +
  theme_minimal()

ggsave("output/county_cd_split_map.png", p, width = 8, height = 6.5, dpi = 120)
message("Wrote output/county_cd_split_map.png")
