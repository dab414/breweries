usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))
summary_data <- read.csv('summary_data/small_data/beer_summary_data.csv')

## dunno if this will work
# https://github.com/ThinkR-open/golem/blob/master/R/use_favicon.R
#source('www/use_favicon.R')
#use_favicon(path = 'www/favicon.ico')

server <- function(input, output){
  
  ## process incoming zipcode, return appropriate rows from centroid data

  rv <- reactiveValues(
    is_bad_zip = FALSE,
    new_search = TRUE,
    init = TRUE,
    user_selected = TRUE
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
      rv$init <- TRUE
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


  ## FILTER DATA BASED ON MARKER CLICK
  observeEvent(input$mainResult_marker_click, {
    click <- input$mainResult_marker_click

    if (click$id == 'user') {
      rv$user_selected <- TRUE
    } else rv$user_selected <- FALSE

    centroid_data$rel_data <- centroid_data$data[centroid_data$data$id == click$id,]
    rv$new_search <- FALSE

  })  
  
  
  ## MANAGE USER AND COMPETITION INFO BOXES
  source('server/competitionMatcher/infoBox/infoBoxFunctions.r', local = TRUE)
  

  output$competition_top_beer_title <- renderText(
    return(paste('Top scoring beers in ', centroid_data$rel_data$city, ', ',
                        centroid_data$rel_data$state_abbrv, ':', sep = ''))
  )

  output$bad_query <- renderText({
    if (rv$init | rv$is_bad_zip) {
      return('Enter a zipcode and select a competition area before coming to this tab.')
    } else if (rv$new_search | rv$user_selected) {
      return('Select a competition area on the map to view the top beers in that area.')    
    } else return('')

  })


  observe({
    
    ## HIDING THE TAB BOX DOESNT APPLY TO ITS CONTENTS

    if (rv$init | rv$is_bad_zip | rv$new_search | rv$user_selected) {
      shinyjs::hide(id = 'results_container')
      shinyjs::show(id = 'bad_query')
    } else {
      shinyjs::show(id = 'results_container')
      shinyjs::hide(id = 'bad_query')
    }
  })


  output$competition_top_beer_data <- renderTable(
    {
      out <- summary_data[summary_data$label == centroid_data$rel_data$label, 
      c('beer_name', 'beer_type', 'beer_abv', 'beer_num_reviewers', 'beer_beer_date_added', 
        'brewery_name','beer_beer_score')]

      out <- out[order(out$beer_beer_score, decreasing = TRUE),]

      colnames(out) <- c('Beer Name', 'Beer Type', 'ABV', 'Number of Reviews', 'Date Added',
                          'Brewery Name', 'Beer Score')

      out

    },
    width = '100%'
  )

  output$winning_beer_name <- renderText({
    out <- summary_data[summary_data$label == centroid_data$rel_data$label,]
    out <- out[order(out$beer_beer_score, decreasing = TRUE),][1,]

    paste('Review of:', as.character(out$beer_name))
  })

  output$winning_beer_date <- renderText({
    out <- summary_data[summary_data$label == centroid_data$rel_data$label,]
    out <- out[order(out$beer_beer_score, decreasing = TRUE),][1,]

    as.character(out$review_review_date)
  })

  output$top_review <- renderText({

    out <- summary_data[summary_data$label == centroid_data$rel_data$label,]
    out <- out[order(out$beer_beer_score, decreasing = TRUE),][1,]
    #cat(file = stderr(), out)

    as.character(out$review_review_text)
  })


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