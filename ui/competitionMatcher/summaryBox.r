summaryBox <- box(width = 12,
      title = 'General Summary',
      status = 'primary',
      solidHeader = TRUE,`
      
      box(width = 6, id = 'user_box',
         title = h3(textOutput('your_location') %>% withSpinner()),
         #infoBoxOutput('user_location'),
         infoBoxOutput('user_population'),
         infoBoxOutput('user_median_age'),
         infoBoxOutput('user_total_water')
          ),
      
      box(width = 6, id ='comp_box',
          title = h3(textOutput('competition_location')),
          infoBoxOutput('comp_population'),
          infoBoxOutput('comp_median_age'),
          infoBoxOutput('comp_total_water')
          )
      )