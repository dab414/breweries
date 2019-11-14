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
              h3(textOutput('winning_beer_name')),
              p(textOutput('winning_beer_date')),
              div(textOutput('top_review'), style = 'font-size: 200%')
            
          )
        )
      )

      tabPanel(
        title = 'Brewery Analyzer',
        fluidRow(
          h3('See what people are saying about the beers from different breweries.'),
          p('Selecting a brewery from the map on the left will show you the words that people most often use in reviews to describe beers from that brewery. The breweries on the map are color-coded by success [update this part].')
        ),

        fluidRow(
          ## MAP
          column(width = 6,
            leafletOutput('brewery_map')
          ),

          ## WORDCLOUD
          column(width = 6,
            plotOutput('wordcloud')
          )
        )

      )


    )
  )
)