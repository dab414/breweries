usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))


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

  busy <- reactiveValues(
    is_busy = FALSE
  )

  centroid_data <- reactiveValues()
  beer_data <- reactiveValues(
    all = read.csv('summary_data/small_data/beer_summary_data.csv')
  )


  output$mainResult <- renderLeaflet({
      leaflet(usa_bbox) %>% addTiles() %>% 
      fitBounds(~min(longitude), ~min(latitude), ~max(longitude), ~max(latitude)) 
  })

  observe({
    shinyjs::hide(id = 'zip_processing')
  })
  
  observeEvent(input$submitButton, {
    ## CONTROL THE LOADING PANEL
    shinyjs::hide(id = 'zip_ready')
    shinyjs::show(id = 'zip_processing')
    
    source_python('get_similar_regions_from_zip.py')
    centroid_data$data <- zip_to_similar(input$textMe)
    
    shinyjs::show(id = 'zip_ready')
    shinyjs::hide(id = 'zip_processing')      

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

    ## condense beer data
    beer_data$rel_data <- beer_data$all[beer_data$all$label == centroid_data$rel_data$label,]
    

    ### NEED TO ADD THE REVIEW COLUMNS HERE
    beer_data$rel_data <- beer_data$rel_data[,c('beer_name', 'beer_type', 
        'beer_abv', 'beer_num_reviewers', 'beer_beer_date_added', 
        'brewery_name','beer_beer_score', 'review_review_date', 'review_review_text')]
    beer_data$rel_data <- beer_data$rel_data[order(beer_data$rel_data$beer_beer_score,
      decreasing = TRUE),]

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
    ## SHOW OR HIDE ALL THE ANALYSIS STUFF

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
      out <- beer_data$rel_data[, c('beer_name', 'beer_type', 
        'beer_abv', 'beer_num_reviewers', 'beer_beer_date_added', 
        'brewery_name','beer_beer_score')]

      out <- out[order(out$beer_beer_score, decreasing = TRUE),]

      colnames(out) <- c('Beer Name', 'Beer Type', 'ABV', 'Number of Reviews', 'Date Added',
                          'Brewery Name', 'Beer Score')

      out

    },
    width = '100%'
  )

  output$winning_beer_name <- renderText({
    paste('Review of:', as.character(beer_data$rel_data$beer_name)[1])
  })

  output$winning_beer_date <- renderText({
    as.character(beer_data$rel_data$review_review_date[1])
  })

  output$top_review <- renderText({
    as.character(beer_data$rel_data$review_review_text[1])
  })



## FAILED
  # output$review_tabs <- renderUI({

  #   beer_data$rel_data <- beer_data$rel_data[order(beer_data$rel_data$beer_beer_score, 
  #     decreasing = TRUE),]

  #   reviewTabs <- lapply(
  #       as.character(beer_data$rel_data$beer_name),
  #      tabPanel, 
  #         arg1 = lapply(paste('Review of:', beer_data$rel_data$beer_name), h3),
  #         arg2 = lapply(beer_data$rel_data$review_review_date, p),
  #         arg3 = lapply(beer_data$rel_data$review_review_text, div)
  #   )

  #   do.call(tabsetPanel, reviewTabs)

  # })


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