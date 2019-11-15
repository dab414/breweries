
output$brewery_map <- renderLeaflet({
  ## i need to be able to reference cluster ID here
  click <- input$mainResult_marker_click
  active_label <- centroid_data$data[centroid_data$data$id == click$id,]$label
  beer_data$rel_review_data <- breweries[breweries$label == active_label,]


  leaflet(beer_data$rel_review_data) %>%
  addTiles() %>%
  fitBounds(~min(longitude) - 1, ~min(latitude) - 1, ~max(longitude) + 1, ~max(latitude) + 1) 

})