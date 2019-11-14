
output$brewery_map <- renderLeaflet({
  ## i need to be able to reference cluster ID here
  rel_breweries <- beer_data$big %>%


  leaflet()

})