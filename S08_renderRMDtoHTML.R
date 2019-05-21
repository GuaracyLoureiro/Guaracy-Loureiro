#!/usr/bin/Rscript

pkgCheck <- function(packages){
    for(x in packages){
        try(if (!require(x, character.only = TRUE)){
            install.packages(x, dependencies = TRUE)
            if(!require(x, character.only = TRUE)) {
                stop()
            }
        })
    }
}
pkgCheck(c("flexdashboard", "ggplot2", "gridExtra", "rmarkdown"))

setwd("/your/path/")

rmarkdown::render(input = 'dashboard_DAY.Rmd', output_file = paste0('sElevage_DAY.html'))
rmarkdown::render(input = 'dashboard_WEEK.Rmd', output_file = paste0('sElevage_WEEK.html'))
rmarkdown::render(input = 'dashboard_MONTH.Rmd', output_file = paste0('sElevage_MONTH.html'))
