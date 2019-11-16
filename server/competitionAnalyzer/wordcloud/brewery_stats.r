
observe({
  if (rv$show_brewery_stats) {
    shinyjs::show(id = 'brewery_stats_box')
  } else shinyjs::hide(id = 'brewery_stats_box')
})


observeEvent(input$breweryMap_marker_click, {
  rv$show_brewery_stats = TRUE
  beer_data$rel_beer_data <- beer_data$small[beer_data$small$brewery_id == input$breweryMap_marker_click$id,]
})


output$breweryName <- renderText({beer_data$rel_beer_data$brewery_name})
output$avgBeerRating <- renderText({paste('Average beer rating:', round(beer_data$rel_beer_data$beer_rating_avg, 2))})
output$twitterFollowers <- renderText({paste('Number of Twitter followers:', beer_data$rel_beer_data$twitter_followers_count)})
output$percentileRank <- renderText({

  all_competition <- beer_data$small[beer_data$small$label == beer_data$rel_beer_data$label, c('brewery_id', 'composite_success')]
  all_competition <- all_competition[order(all_competition$composite_success, decreasing = TRUE),]
  rownames(all_competition) <- 1:(nrow(all_competition))
  rank <- which(all_competition$brewery_id == beer_data$rel_beer_data$brewery_id)

  percentile <- ((nrow(all_competition) - rank) / nrow(all_competition)) * 100

  paste('Percentile rank:', round(percentile, 2))

})
output$breweryType <- renderText({paste('Brewery type: ', beer_data$rel_beer_data$brewery_type)})
output$breweryAddress <- renderText({paste('Brewery address: ', beer_data$rel_beer_data$address)})
output$beerCount <- renderText({paste('Beer count: ', beer_data$rel_beer_data$beer_count)})
output$reviewCount <- renderText({paste('Review count: ', beer_data$rel_beer_data$review_count)})