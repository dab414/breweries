usa_bbox <- data.frame(latitude = c(23.725012, 49.239121), longitude = c(-125.771484,-66.2695311))

server <- function(input, output){
  
  ## process incoming zipcode, return appropriate rows from centroid data

  snake <- eventReactive(input$submitButton, {
    source_python('get_similar_regions_from_zip.py')
    zip_to_similar(input$textMe)
  })  

  #output$invalid_zipcode <- renderText(invalid_zipcode())
  output$invalid_zipcode <- renderText({
     if (typeof(snake()) == 'character') {
        snake()
     }  else {
        ''
      }
    })

  valid_data <- eventReactive(snake(), {
    if (typeof(snake()) == 'list') {
      snake
    }
  })


  #observe({cat(file = stderr(), snake())})
  
  #### COMPETITION MATCHER ####

  ## ADD MARKERS IN RESPONSE TO ZIPCODE INPUT
  ## Watch for marker click, return appropriate row from centroid data
  source('server/competitionMatcher/map/mapFunctions.r', local = TRUE)
  
  ## MANAGE USER AND COMPETITION INFO BOXES
  source('server/competitionMatcher/infoBox/infoBoxFunctions.r', local = TRUE)
  



  #### COMPETITION ANALYZER ####


}