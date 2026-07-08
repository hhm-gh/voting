# One-time setup: installs packages via renv. Run once after cloning:
#   Rscript setup.R
# (or source("setup.R") from within RStudio after opening voting.Rproj)

if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv")
renv::restore()
