library(shiny)
library(shinyjs)
library(ggplot2)
library(reticulate)
library(dplyr)
library(shinycssloaders)
library(shinydashboard)
library(leaflet)
library(htmltools)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)
library(data.table)

source('ui/ui.r')
source('server/server.r')

packages <- c('pandas', 'numpy', 'requests', 'bs4', 'progressbar', 'sklearn')

# use_python('/usr/bin/python3')
# py_install(c('pandas', 'requests', 'bs4'))

virtualenv_create(envname = 'python_environment', python = 'python3')
virtualenv_install('python_environment', packages = packages)
reticulate::use_virtualenv('python_environment', required = TRUE)








shinyApp(ui = ui, server = server)

  