
observe({

  current_brewery <- input$breweryMap_marker_click$id
  d <- beer_data$beers[beer_data$beers$brewery_id == current_brewery,]
  
  common_types <- d %>%
    group_by(beer_type) %>%
    summarize(count = n()) %>%
    filter(count >= 2)

  d <- d %>%
    inner_join(common_types) 

  common_types <- common_types$beer_type

  d <- d[d$beer_type %in% common_types,]

  beer_data$rel_beer <- d

  if (nrow(d) >= 2 & rv$show_brewery_stats) {
    shinyjs::show(id = 'beer_abv')
  } else {
    shinyjs::hide(id = 'beer_abv')
  }

})



output$abv_type <- renderPlot({
  
  d <- beer_data$rel_beer

  if (nrow(d) > 50) {
    d %>%
    filter(count >= 5) %>%
    ggplot(aes(x = as.numeric(beer_abv), y = reorder(beer_type, -count))) + 
      geom_density_ridges(aes(fill = count), alpha = .7) +
      xlab('Beer Alcohol Percentage') + ylab('Beer Type') +
      scale_fill_continuous(name = 'Number of Beers') + 
      theme_bw() +
      theme(text = element_text(size = 20))

  } else if (nrow(d) > 0 & nrow(d) <= 50) {
    d %>%
    group_by(beer_type) %>%
    summarize(count = n()) %>%
    ggplot(aes(x = reorder(beer_type, -count), y = count)) + geom_bar(stat = 'identity') +
    labs(x = 'Beer Type', y = 'Count') + 
    theme_bw() +
    theme(text = element_text(size = 20)) +
    coord_flip()
  } 

})