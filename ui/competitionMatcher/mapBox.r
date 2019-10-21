mapBox <- box(title = 'Welcome to the competition matcher.',
  status = 'primary',
  solidHeader = TRUE,
  width = 12,
  
  fluidRow(
    column(10, 
           #h1('Welcome to the competition matcher.'),
           h3('To begin analyzing brewery compeition areas that are similar to yours, enter your zip code below.')
    )
  ),
  
  fluidRow(
  
    column(width = 12,
           
      tags$head(tags$style(type="text/css", "
           #loadmessage {
             position: fixed;
             top: 0px;
             left: 0px;
             width: 100%;
             padding: 5px 0px 5px 0px;
             text-align: center;
             font-weight: bold;
             font-size: 100%;
             color: #ffffff;
             background-color: #0275D8;
             z-index: 105;
           }
        ")),
      
      leafletOutput('mainResult'),# %>% withSpinner(),
      
      absolutePanel(top = 100, left = 100, class = 'panel panel-default', draggable = TRUE, width = 180, height = 160,
                    column(width = 12,
                      p('Enter a valid US zip code'),
                      textOutput('invalid_zipcode'),
                      textInput(inputId = 'textMe', label = '', placeholder = '00000', width = '100px'),
                      actionButton('submitButton', 'Submit'))
                    ),
      
      conditionalPanel(condition = "$('html').hasClass('shiny-busy')",
                       tags$div("Please wait. Processing massive amounts of data.", id = 'loadmessage'))
  )
)
)