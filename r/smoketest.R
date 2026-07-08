# Phase 1 boundary smoke test — loads every processed boundary dataset,
# prints sanity stats, and plots each to r/output/ (gitignored) so mistakes
# (wrong CRS, corrupt geometries, wrong file) are visible before building
# anything on top of this data. Run from the r/ directory:
#   Rscript smoketest.R

library(sf)
library(ggplot2)

source("load.R")

OUTPUT_DIR <- "output"
dir.create(OUTPUT_DIR, showWarnings = FALSE)

datasets <- list(
  list(name = "congressional", cycle = "2021", expected_n = 8),
  list(name = "state_senate", cycle = "2021", expected_n = 35),
  list(name = "state_house", cycle = "2021", expected_n = 65),
  list(name = "counties", cycle = "2024", expected_n = 64),
  list(name = "denver_council_districts", cycle = "2024", expected_n = 13)
)

for (d in datasets) {
  message(sprintf("\n=== %s (%s) ===", d$name, d$cycle))
  boundaries <- load_boundary(d$name, d$cycle)

  if (nrow(boundaries) != d$expected_n) {
    warning(sprintf(
      "%s: expected %d features, got %d", d$name, d$expected_n, nrow(boundaries)
    ))
  } else {
    message(sprintf("  feature count OK (%d)", nrow(boundaries)))
  }

  bbox <- st_bbox(boundaries)
  message(sprintf(
    "  bbox: [%.2f, %.2f, %.2f, %.2f]", bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
  ))
  # Colorado's real-world bbox is roughly lon -109..-102, lat 37..41 —
  # a quick eyeball check that we're not looking at State Plane feet or
  # some other unprojected mess that slipped through.
  in_colorado_bbox <- bbox["xmin"] > -110 && bbox["xmax"] < -101 &&
    bbox["ymin"] > 36 && bbox["ymax"] < 42
  if (!in_colorado_bbox) {
    warning(sprintf("%s: bbox looks outside Colorado — check CRS/reprojection", d$name))
  }

  p <- ggplot(boundaries) +
    geom_sf(fill = "steelblue", color = "white", linewidth = 0.2) +
    labs(title = sprintf("%s (%s)", d$name, d$cycle)) +
    theme_minimal()

  out_path <- file.path(OUTPUT_DIR, sprintf("%s_%s.png", d$name, d$cycle))
  ggsave(out_path, p, width = 7, height = 6, dpi = 100)
  message(sprintf("  wrote %s", out_path))
}

message("\nSmoke test complete — check r/output/*.png for visual sanity.")
