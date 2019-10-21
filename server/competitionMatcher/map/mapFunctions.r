## initialize map
  output$mainResult <- renderLeaflet({
      leaflet(usa_bbox) %>% addTiles() %>% fitBounds(~min(longitude), ~min(latitude), ~max(longitude), ~max(latitude)) 
    })

## ADD MARKERS IN RESPONSE TO ZIPCODE INPUT
observeEvent(valid_data(), {
    #pal <- colorFactor(c("navy", "red"), domain = c("ship", "pirate"))
    
    ## ^ https://stackoverflow.com/questions/33027756/hide-an-element-box-tabs-in-shiny-dashboard
    label = rep(0, 4)
    
    for (row in 1:(nrow(valid_data()()))){
      population <- valid_data()()$total_population[row] / 1000
      population <- ifelse(population < 1, 'Population: < 1k', paste('Population: ', round(population), 'k', sep=''))
      label[row] <- paste(ifelse(valid_data()()$id[row] == 'user', HTML('<b>Your Location</b>'), HTML('<b>Competition</b>')), paste(valid_data()()$city[row], ', ', valid_data()()$state_abbrv[row], sep=''), population, sep = HTML('<br/>'))  
    }
    
    in_data <- valid_data()()
    in_data$popup <- label
    
    leafletProxy('mainResult', data = in_data) %>% 
      clearShapes() %>% 
      addCircleMarkers(color = ~ifelse(id == 'user', 'blue', 'green'), stroke = FALSE, fillOpacity = .6, popup = ~popup, layerId = ~id)
    
  })  


observe({cat(file = stderr(), input$mainResult_marker_click$id)})

competitionData <- eventReactive(valid_data(), {
    show(id = 'comp_box')
    cat(file = stderr(), 'line 33 running')
    return('Click on a competition area to view the comparison')
  })

## Watch for marker click, return appropriate row from centroid data
competitionData <- eventReactive(input$mainResult_marker_click, {
  click <- input$mainResult_marker_click
  
  cat(file = stderr(), 'running')

  if (click$id == 'user') {
    return('Click on a competition area to view the comparison')
  } else if (!is.null(click)) {
    show(id = 'comp_box')
    return(valid_data()()[valid_data()()$id == click$id,])
  }
})