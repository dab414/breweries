mapBox <- box(title = 'Welcome to Better Brewery.',
  status = 'primary',
  solidHeader = TRUE,
  width = 12,
  
  fluidRow(
    column(10, 
           #h1('Welcome to the competition matcher.'),
           h3('To begin exploring breweries, enter your zip code below.'),
           p("You can then explore breweries in your area, or you can explore breweries that are in areas that are similar to your area.")
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
      
      absolutePanel(top = 100, left = 100, class = 'panel panel-default', id='zip_ready',
        draggable = TRUE, width = 180, height = 160,
        column(
          width = 12,
          p('Enter a valid US zip code'),
          textInput(inputId = 'textMe', label = '', placeholder = '00000', width = '100px'),
          actionButton('submitButton', 'Submit')
        )
      ),

      absolutePanel(top = 100, left = 100, class = 'panel panel-default', id='zip_processing',
        draggable = TRUE, width = 180, height = 160,
        column(
          width = 12,
          p('Please wait. Processing massive amounts of data.'),
          div(tags$img(src = 'loading.gif', height = '75px', width = '75px'), 
            style = 'text-align: center')
        )
        
      ),
      
      conditionalPanel(condition = "$('html').hasClass('shiny-busy')",
                       tags$div("Please wait. Processing massive amounts of data.", id = 'loadmessage'))
  )
)
)