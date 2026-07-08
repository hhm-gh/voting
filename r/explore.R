# Interactive exploration — open any processed boundary as a zoomable
# Leaflet-style map in RStudio's Viewer pane (or a browser tab if run via
# Rscript). Nicer than the static smoketest.R plots for actually poking
# around a dataset.
#
# Usage (from RStudio, with r/voting.Rproj open):
#   source("explore.R")
#   mapview(load_boundary("denver_council_districts", "2024"))
#   mapview(load_boundary("congressional", "2021"))

library(mapview)
source("load.R")
