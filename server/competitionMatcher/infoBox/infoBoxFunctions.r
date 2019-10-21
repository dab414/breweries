## USER LOCATION STATS

  output$your_location <- renderText({
     paste(valid_data()()[valid_data()()$id == 'user',]$city, ', ', valid_data()()[valid_data()()$id == 'user',]$state_long, sep = '')
  })

  output$user_population <- renderInfoBox({
    infoBox('Population', format(valid_data()()[valid_data()()$id == 'user',]$total_population, big.mark = ','), icon = icon('user', lib = 'glyphicon'), color = 'green')
  })
  
  
  output$user_median_age <- renderInfoBox({
    infoBox('Median Age', valid_data()()[valid_data()()$id == 'user',]$median_age, icon = icon('info-sign', lib = 'glyphicon'), color = 'blue')
  })

  output$user_total_water <- renderInfoBox({
    infoBox('Water Contams', format(valid_data()()[valid_data()()$id == 'user',]$total_water_count, big.mark = ','), icon = icon('warning-sign', lib = 'glyphicon'), color = 'orange')
  })
  

  
  
  ## COMPETITION STATS
  output$competition_location <- renderText({
    if (typeof(competitionData()) == 'character'){
      cat(file = stderr(), 'line 26 running')
      hide(id = 'comp_box')
      #show(id = 'comp_box')
      return(competitionData())
    } else {
      show(id = 'comp_box')
      return(paste(competitionData()$city, ', ', competitionData()$state_long, sep = ''))
    }
  })
  
  output$comp_population <- renderInfoBox({
    if (typeof(competitionData()) == 'list') 
      infoBox('Population', format(valid_data()()[valid_data()()$id == input$mainResult_marker_click$id,]$total_population, big.mark = ','), icon = icon('user', lib = 'glyphicon'), color = 'green')
  })
  output$comp_median_age <- renderInfoBox({
    if (typeof(competitionData()) == 'list') 
      infoBox('Median Age', valid_data()()[valid_data()()$id == input$mainResult_marker_click$id,]$median_age, icon = icon('info-sign', lib = 'glyphicon'), color = 'blue')
  })
  output$comp_total_water <- renderInfoBox({
    if (typeof(competitionData()) == 'list') 
      infoBox('Water Contams', format(valid_data()()[valid_data()()$id == input$mainResult_marker_click$id,]$total_water_count, big.mark = ','), icon = icon('warning-sign', lib = 'glyphicon'), color = 'orange')
  })