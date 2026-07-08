library(sf)

# Root of the data directory (relative to the r/ folder)
DATA_ROOT <- file.path(dirname(getwd()), "data")

# Load a processed boundary dataset, e.g. load_boundary("congressional", "2021")
# Tries GeoParquet first (the documented primary format), falls back to
# GeoPackage if that fails — see OVERVIEW.md's Architecture section for why
# both are written by scripts/process_phase1_boundaries.py.
load_boundary <- function(name, cycle) {
  dir <- file.path(DATA_ROOT, "processed", name, cycle)
  parquet_path <- file.path(dir, "boundaries.geoparquet")
  gpkg_path <- file.path(dir, "boundaries.gpkg")

  result <- tryCatch(
    {
      sf_obj <- st_read(parquet_path, quiet = TRUE)
      message(sprintf("Loaded '%s' (%s) from GeoParquet", name, cycle))
      sf_obj
    },
    error = function(e) {
      if (!file.exists(gpkg_path)) stop(e)
      message(sprintf(
        "GeoParquet read failed for '%s' (%s), falling back to GeoPackage: %s",
        name, cycle, conditionMessage(e)
      ))
      st_read(gpkg_path, quiet = TRUE)
    }
  )

  message(sprintf(
    "  %d features | CRS: %s", nrow(result), st_crs(result)$input
  ))
  result
}
