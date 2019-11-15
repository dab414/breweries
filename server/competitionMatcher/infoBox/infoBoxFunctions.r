### MANAGE DISPLAYING THE BOXES
observe({

  if (rv$is_bad_zip | rv$init) {
    shinyjs::hide(id = 'user_box') 
    } else shinyjs::show(id = 'user_box')

  if (rv$is_bad_zip | rv$init | rv$new_search | rv$user_selected) {
    shinyjs::hide(id = 'comp_box') 
  } else shinyjs::show(id = 'comp_box') 

})


## USER LOCATION STATS

  output$your_location <- renderText({
    if (!rv$is_bad_zip & !rv$init)
    paste(centroid_data$data[centroid_data$data$id == 'user',]$city, ', ', 
      centroid_data$data[centroid_data$data$id == 'user',]$state_long, sep = '')
  })

  output$user_population <- renderInfoBox({
    infoBox('Population', format(centroid_data$data[centroid_data$data$id == 'user',]$total_population, 
      big.mark = ','), icon = icon('user', lib = 'glyphicon'), color = 'green')
  })
  
  output$user_median_age <- renderInfoBox({
    infoBox('Median Age', centroid_data$data[centroid_data$data$id == 'user',]$median_age, icon = icon('info-sign', lib = 'glyphicon'), color = 'blue')
  })

  output$user_total_water <- renderInfoBox({
    infoBox('Water Contams', format(centroid_data$data[centroid_data$data$id == 'user',]$total_water_count, big.mark = ','), icon = icon('warning-sign', lib = 'glyphicon'), color = 'orange')
  })
  
  ## COMPETITION STATS
  output$competition_location <- renderText({
    if (!rv$is_bad_zip & !rv$init & !rv$new_search & !rv$user_selected)
    return(paste(centroid_data$rel_summary_data$city, ', ', centroid_data$rel_summary_data$state_long, sep = ''))
  })
  output$comp_population <- renderInfoBox({
    infoBox('Population', format(centroid_data$rel_summary_data[centroid_data$rel_summary_data$id == input$mainResult_marker_click$id,]$total_population, big.mark = ','), 
      icon = icon('user', lib = 'glyphicon'), color = 'green')
  })
  output$comp_median_age <- renderInfoBox({
   infoBox('Median Age', centroid_data$rel_summary_data[centroid_data$rel_summary_data$id == input$mainResult_marker_click$id,]$median_age, 
    icon = icon('info-sign', lib = 'glyphicon'), color = 'blue')
  })
  output$comp_total_water <- renderInfoBox({
  
    infoBox('Water Contams', format(centroid_data$rel_summary_data[centroid_data$rel_summary_data$id == input$mainResult_marker_click$id,]$total_water_count, big.mark = ','), 
      icon = icon('warning-sign', lib = 'glyphicon'), color = 'orange')
  })