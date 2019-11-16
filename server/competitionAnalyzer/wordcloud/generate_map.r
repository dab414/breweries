
output$breweryMap <- renderLeaflet({
  
  click <- input$mainResult_marker_click
  active_label <- centroid_data$data[centroid_data$data$id == click$id,]$label
  #beer_data$rel_review_data <- beer_data$small[beer_data$small$label == active_label,]
  d <- beer_data$small[beer_data$small$label == active_label,]

  d <- d[order(d$composite_success, decreasing = TRUE),]
  row.names(d) <- 1:(nrow(d))
  num_rows <- nrow(d)
  d$percentile <- ((num_rows - as.numeric(rownames(d))) / num_rows) 

  leaflet(d) %>%
  addTiles() %>%
  fitBounds(~min(longitude) - 0.01, ~min(latitude) - 0.01, ~max(longitude) + 0.01, ~max(latitude) + 0.01) %>%
  clearShapes() %>%
  addCircleMarkers(stroke = FALSE, fillOpacity = .6, color = ~ifelse(percentile > .5, 'green', 'brown'),
    popup = ~brewery_name, layerId = ~brewery_id)

})