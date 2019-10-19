library(shiny)
library(ggplot2)
library(reticulate)
library(dplyr)
library(shinycssloaders)
library(shinydashboard)
library(leaflet)
library(htmltools)

packages <- c('pandas', 'numpy', 'requests', 'bs4', 'progressbar')

# use_python('/usr/bin/python3')
# py_install(c('pandas', 'requests', 'bs4'))

virtualenv_create(envname = 'python_environment', python = 'python3')
virtualenv_install('python_environment', packages = packages)
reticulate::use_virtualenv('python_environment', required = TRUE)


usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))

ui <- dashboardPage(
  dashboardHeader(title = 'Get your insights here'),
  dashboardSidebar(),
  dashboardBody(
    box(title = 'Welcome to the competition matcher.',
        status = 'primary',
        solidHeader = TRUE,
        width = 12,
        
        fluidRow(
          column(10, 
                 #h1('Welcome to the competition matcher.'),
                 h3('To begin analyzing brewery compeition areas that are similar to yours, enter your zip code below.')
          )
        ),
        
        fluidRow(
        
          column(width = 12,
           
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
            leafletOutput('mainResult'),# %>% withSpinner(),
            
            absolutePanel(top = 100, left = 100, class = 'panel panel-default', draggable = TRUE, width = 180, height = 160,
                          column(width = 12,
                            p('Enter a valid US zip code'),
                            textInput(inputId = 'textMe', label = '', placeholder = '00000', width = '100px'),
                            actionButton('submitButton', 'Submit'))
                          ),
            
            conditionalPanel(condition = "$('html').hasClass('shiny-busy')",
                             tags$div("Please wait. Processing massive amounts of data.", id = 'loadmessage'))
        )
      )
    ),
  
  box(width = 12,
      title = 'General Summary',
      status = 'primary',
      solidHeader = TRUE,
      
      box(width = 6,
             title = h3(textOutput('your_location')),
             #infoBoxOutput('user_location'),
             infoBoxOutput('user_population'),
             infoBoxOutput('user_median_age'),
             infoBoxOutput('user_total_water')
             ),
      
      box(width = 6,
             #h3(textOutput()),
             #infoBoxOutput('user_population')
             )
      ),  
  
  box(width = 12,
      title = 'Output data',
      status = 'primary',
      solidHeader = TRUE,
      tableOutput('criticalData') %>%  withSpinner()
      )
)
)

server <- function(input, output){
  
  snake <- eventReactive(input$submitButton, {
    source_python('get_similar_regions_from_zip.py')
    zip_to_similar(input$textMe)
    })
  
  output$mainResult <- renderLeaflet({
      leaflet(usa_bbox) %>% addTiles() %>% fitBounds(~min(longitude), ~min(latitude), ~max(longitude), ~max(latitude)) 
    })
  
  
  observe({
    #pal <- colorFactor(c("navy", "red"), domain = c("ship", "pirate"))
    
    label = rep(0, 4)
    
    for (row in 1:(nrow(snake()))){
      population <- snake()$total_population[row] / 1000
      population <- ifelse(population < 1, 'Population: < 1k', paste('Population: ', round(population), 'k', sep=''))
      label[row] <- paste(ifelse(snake()$id[row] == 'user', HTML('<b>Your Location</b>'), HTML('<b>Competition</b>')), paste(snake()$city[row], ', ', snake()$state_abbrv[row], sep=''), population, sep = HTML('<br/>'))  
    }
    
    in_data <- snake()
    in_data$popup <- label
    
    leafletProxy('mainResult', data = in_data) %>% 
      clearShapes() %>% 
      addCircleMarkers(color = ~ifelse(id == 'user', 'blue', 'green'), stroke = FALSE, fillOpacity = .6, popup = ~popup)
    
  })
  
  
     output$your_location <- renderText({
       paste(snake()[snake()$id == 'user',]$city, ', ', snake()[snake()$id == 'user',]$state_long, sep = '')
     })
  
  
    output$user_population <- renderInfoBox({
      infoBox('Population', format(snake()[snake()$id == 'user',]$total_population, big.mark = ','), icon = icon('user', lib = 'glyphicon'), color = 'green')
    })
    
    output$user_median_age <- renderInfoBox({
      infoBox('Median Age', snake()[snake()$id == 'user',]$median_age, icon = icon('info-sign', lib = 'glyphicon'), color = 'blue')
    })
    
    output$user_total_water <- renderInfoBox({
      infoBox('Water Contams', format(snake()[snake()$id == 'user',]$total_water_count, big.mark = ','), icon = icon('warning-sign', lib = 'glyphicon'), color = 'orange')
    })
    
  
  output$criticalData <- renderTable({
    snake()
  })
  
  
}

shinyApp(ui = ui, server = server)

