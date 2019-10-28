competitionAnalyzer <- tabItem(
  tabName = 'competitionAnalyzer',

  h2(textOutput('bad_query')),
  
  box(id = 'results_container', width = 12,
    tabBox(width = 12, id = 'competition_analyzer_results',
      
      tabPanel(
        title = 'Top Beers',

        fluidRow(
          h3(textOutput('competition_top_beer_title')),
          div(tableOutput('competition_top_beer_data'), style = 'font-size: 130%')
        ),


        fluidRow(

          box(width = 12, id = 'review_container',
            
              #title = 'beer1',
              h3(textOutput('winning_beer_name')),
              p(textOutput('winning_beer_date')),
              div(textOutput('top_review'), style = 'font-size: 200%')
            
          )

          #uiOutput('review_tabs')
          
        )
      )
    )
  )
)