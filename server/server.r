usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))

server <- function(input, output){
  
  ## process incoming zipcode, return appropriate rows from centroid data

  rv <- reactiveValues(
    is_bad_zip = FALSE,
    new_search = TRUE,
    init = TRUE
  )

  centroid_data <- reactiveValues()

  output$mainResult <- renderLeaflet({
      leaflet(usa_bbox) %>% addTiles() %>% 
      fitBounds(~min(longitude), ~min(latitude), ~max(longitude), ~max(latitude)) 
  })

  
  observeEvent(input$submitButton, {
    source_python('get_similar_regions_from_zip.py')
    centroid_data$data <- zip_to_similar(input$textMe)

    if (typeof(centroid_data$data) == 'character') {
      rv$is_bad_zip <- TRUE
      return()
    }

    rv$init <- FALSE
    rv$new_search <- TRUE

    ## build the popup label
    population <- centroid_data$data$total_population / 1000
    population <- ifelse(population < 1, 'Population: < 1k', 
      paste('Population: ', round(population), 'k', sep = ''))
    popup <- paste(paste('<b>', centroid_data$data$city, ', ', 
                        centroid_data$data$state_abbrv, '</b>', sep = ''),
                  population, sep = '<br/>')
    centroid_data$data$popup <- popup

    leafletProxy('mainResult', data = centroid_data$data) %>% 
      clearShapes() %>% 
      addCircleMarkers(color = ~ifelse(id == 'user', 'blue', 'green'), 
        stroke = FALSE, fillOpacity = .6, popup = ~popup, layerId = ~id)

  })


  observeEvent(input$mainResult_marker_click, {

    click <- input$mainResult_marker_click
    centroid_data$rel_data <- centroid_data$data[centroid_data$data$id == click$id,]
    rv$new_search <- FALSE

  })  





  #observe({cat(file = stderr(), snake())})
  
  #### COMPETITION MATCHER ####

  ## ADD MARKERS IN RESPONSE TO ZIPCODE INPUT
  ## Watch for marker click, return appropriate row from centroid data
  #source('server/competitionMatcher/map/mapFunctions.r', local = TRUE)
  
  ## MANAGE USER AND COMPETITION INFO BOXES
  source('server/competitionMatcher/infoBox/infoBoxFunctions.r', local = TRUE)
  


  ## CATCH INVALID ZIPS

  observe({
    if (rv$is_bad_zip) {
      showModal(modalDialog(
        title = 'The zip code you entered was invalid. Please try again.',
        easyClose = TRUE,
        footer = NULL
      ))
      rv$is_bad_zip <- FALSE
    }
  })


  #### COMPETITION ANALYZER ####


}