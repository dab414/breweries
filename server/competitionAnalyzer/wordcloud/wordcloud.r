

observe({
  current_brewery <- input$breweryMap_marker_click$id
  rel_review_data <- beer_data$large[beer_data$large$brewery_id == current_brewery, c('brewery_id', 'review_review_text')]
  source_python('text_to_counts.py')
  rv$word_counts <- get_word_counts(rel_review_data)
  if (typeof(rv$word_counts) == 'character') {
    rv$valid_cloud <- FALSE
  } else rv$valid_cloud  <- TRUE

})



output$wordcloud <- renderPlot({

  if (rv$valid_cloud) {
    shinyjs::hide(id = 'bad_cloud')
    shinyjs::show(id = 'wordcloud')

    wordcloud(words = rv$word_counts$word, freq = rv$word_counts$count, #scale = c(2,0.05),
              max.words = 50, random.order = FALSE, rot.per = 0.2,
              colors = brewer.pal(8, 'Dark2'))
  }

})


output$bad_cloud <- renderText({
  
  if (!rv$valid_cloud) {
    
    shinyjs::show(id = 'bad_cloud')
    shinyjs::hide(id = 'wordcloud')
    return(rv$word_counts)
  }

})