usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))
beer_summary_data <- read.csv('summary_data/small_data/beer_summary_data.csv')
#breweries_beers_reviews <- read.csv('summary_data/large_data/breweries_beers_reviews.csv')
#breweries_beers <- read.csv('summary_data/large_data/breweries_beers.csv')
# breweries <- read.csv('summary_data/large_data/breweries.csv')

## dunno if this will work
# https://github.com/ThinkR-open/golem/blob/master/R/use_favicon.R
#source('www/use_favicon.R')
#use_favicon(path = 'www/favicon.ico')

server <- function(input, output, session){
  
  ## process incoming zipcode, return appropriate rows from centroid data

  rv <- reactiveValues(
    is_bad_zip = FALSE,
    new_search = TRUE,
    init = TRUE,
    user_selected = TRUE,
    show_brewery_stats = FALSE
  )

  centroid_data <- reactiveValues()
  beer_data <- reactiveValues(
    large = fread('summary_data/large_data/breweries_beers_reviews.csv'),
    beers = fread('summary_data/large_data/breweries_beers.csv', stringsAsFactors = FALSE),
    small = read.csv('summary_data/large_data/breweries.csv', stringsAsFactors = FALSE)
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
                  population, 
                  ## explore button
                  "<button class=\"btn btn-normal btn-primary\" type = \"button\", onclick = \"Shiny.onInputChange('explore', Math.random())\">Explore</button>",
                  #actionButton(inputId = 'explore_dummy', label = 'Explore', onclick = 'Shiny.onInputChange(\"explore\", Math.random())'),
                  sep = '<br/>')
    centroid_data$data$popup <- popup

    leafletProxy('mainResult', data = centroid_data$data) %>% 
      clearShapes() %>% 
      addCircleMarkers(color = ~ifelse(id == 'user', 'blue', 'green'), 
        stroke = FALSE, fillOpacity = .6, popup = ~popup, layerId = ~id)

  })

  observeEvent(input$explore, {
    # showModal(modalDialog(
    #   title = 'Dicky Horner',
    #   easyClose = TRUE,
    #   footer = NULL
    # ))
    updateTabsetPanel(session, 'tabs', selected = 'competitionAnalyzer')
  })



  ## FILTER DATA BASED ON MARKER CLICK
  observeEvent(input$mainResult_marker_click, {
    click <- input$mainResult_marker_click
    rv$show_brewery_stats <- FALSE

    if (click$id == 'user') {
      rv$user_selected <- TRUE
    } else rv$user_selected <- FALSE

    centroid_data$rel_summary_data <- centroid_data$data[centroid_data$data$id == click$id,]
    rv$new_search <- FALSE

    ## condense beer data
    beer_data$rel_summary_data <- beer_summary_data[beer_summary_data$label == centroid_data$rel_summary_data$label,]
    

    beer_data$rel_summary_data <- beer_data$rel_summary_data[,c('beer_name', 'beer_type', 
        'beer_abv', 'beer_num_reviewers', 'beer_beer_date_added', 
        'brewery_name','beer_beer_score', 'review_review_date', 'review_review_text')]
    beer_data$rel_summary_data <- beer_data$rel_summary_data[order(beer_data$rel_summary_data$beer_beer_score,
      decreasing = TRUE),]

  })  
  
  
  ## MANAGE USER AND COMPETITION INFO BOXES
  source('server/competitionMatcher/infoBox/infoBoxFunctions.r', local = TRUE)
  

  output$competition_top_beer_title <- renderText(
    return(paste('Top scoring beers in ', centroid_data$rel_summary_data$city, ', ',
                        centroid_data$rel_summary_data$state_abbrv, ':', sep = ''))
  )

  output$bad_query <- renderText({
    if (rv$init | rv$is_bad_zip) {
      return('Enter a zipcode and select a competition area before coming to this tab.')
    } else if (rv$new_search | rv$user_selected) {
      return('Select a competition area on the map to view the top beers in that area.')    
    } else return('')

  })

  ## MANAGE WORDCLOUD ANALYZER
  source('server/competitionAnalyzer/wordcloud/generate_map.r', local = TRUE)
  source('server/competitionAnalyzer/wordcloud/brewery_stats.r', local = TRUE)
  source('server/competitionAnalyzer/wordcloud/wordcloud.r', local = TRUE)
  source('server/competitionAnalyzer/wordcloud/generate_ridges.r', local = TRUE)


  observe({
    ## SHOW OR HIDE ALL THE ANALYSIS STUFF

    if (rv$init | rv$is_bad_zip | rv$new_search) {
      shinyjs::hide(id = 'results_container')
      shinyjs::show(id = 'bad_query')
    } else {
      shinyjs::show(id = 'results_container')
      shinyjs::hide(id = 'bad_query')
    }
  })


  output$competition_top_beer_data <- renderTable(
    {
      out <- beer_data$rel_summary_data[, c('beer_name', 'beer_type', 
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
    paste('Review of:', as.character(beer_data$rel_summary_data$beer_name)[1])
  })

  output$winning_beer_date <- renderText({
    as.character(beer_data$rel_summary_data$review_review_date[1])
  })

  output$top_review <- renderText({
    as.character(beer_data$rel_summary_data$review_review_text[1])
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

}