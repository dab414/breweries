output$wordcloud <- renderPlot({

  current_brewery <- input$breweryMap_marker_click$id
  rel_review_data <- beer_data$large[beer_data$large$brewery_id == current_brewery, c('brewery_id', 'review_review_text')]
  source_python('Phase2-RecommendStrategy/review_analysis/text_to_counts.py')
  word_counts <- get_word_counts(rel_review_data)

  wordcloud(words = word_counts$word, freq = word_counts$count, scale = c(2,0.05),
            max.words = 35, random.order = FALSE, rot.per = 0.2,
            colors = brewer.pal(8, 'Dark2'))

})