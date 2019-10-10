library(shiny)
library(ggplot2)
library(reticulate)
library(dplyr)
library(shinycssloaders)

packages <- c('pandas', 'numpy', 'requests', 'bs4')

# use_python('/usr/bin/python3')
# py_install(c('pandas', 'requests', 'bs4'))

virtualenv_create(envname = 'python_environment', python = 'python3')
virtualenv_install('python_environment', packages = packages)
reticulate::use_virtualenv('python_environment', required = TRUE)



ui <- fluidPage(
  titlePanel('Find Matching Competition Areas for your Brewery'),
  
  sidebarLayout(
    sidebarPanel(
      textInput(inputId = 'textMe', label = 'Enter a valid US zip code.', placeholder = '00000', width = '100px'),
      actionButton('submitButton', 'Submit')
    ),
    mainPanel(
      tags$head(tags$style(type="text/css", "
             #loadmessage {
               position: fixed;
               top: 0px;
               left: 0px;
               width: 100%;
               padding: 5px 0px 5px 0px;
               text-align: center;
               font-weight: bold;
               font-size: 100%;
               color: #ffffff;
               background-color: #0275D8;
               z-index: 105;
             }
          ")),
      tableOutput('mainResult') %>% withSpinner(),
      conditionalPanel(condition = "$('html').hasClass('shiny-busy')",
                       tags$div("Please wait. Processing massive amounts of data.", id = 'loadmessage'))
    )
  )
)

server <- function(input, output){
  
  snake <- eventReactive(input$submitButton, {
    source_python('Phase1-FindSimilarCompetitionRegions/get_similar_regions_from_zip.py')
    zip_to_similar(input$textMe)
  })
  
  output$mainResult <- renderTable({
      data.frame(snake())
    })
  
  
}

shinyApp(ui = ui, server = server)

