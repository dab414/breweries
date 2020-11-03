competitionAnalyzer <- tabItem(
  tabName = 'competitionAnalyzer',
  value = 'competitionAnalyzer_value',

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
      ),

      tabPanel(
        title = 'Brewery Analyzer',
        fluidRow(
          h3('See what people are saying about the beers from different breweries.'),
          p('Selecting a brewery from the map on the left will show you the words that people most often use in reviews to describe beers from that brewery. You will also see a visualization about features of the beers at the brewery at the bottom of the page (if the brewery has enough beers).')
        ),

        fluidRow(
          ## MAP
          box(width = 4,
            leafletOutput('breweryMap'),
            p('Breweries marked in green are considered to be more successful based on their average beer rating and number of Twitter followers.')
          ),

          ## WORDCLOUD
          box(width = 8, id = 'brewery_stats_box',
            column(width = 6, 
              h2(textOutput('breweryName')),
              h3('Success Metrics:'),
              p(textOutput('avgBeerRating')),
              p(textOutput('twitterFollowers')),
              p(textOutput('percentileRank')),
              h3('General Information:'),
              p(textOutput('breweryType')),
              p(textOutput('breweryAddress')),
              p(textOutput('beerCount')),
              p(textOutput('reviewCount'))
            ),


            column(width = 6,
              plotOutput('wordcloud'),
              textOutput('bad_cloud')
            )
          )
        ),
        
        fluidRow(
          box(width = 12,

            plotOutput('abv_type')

          )

        )
      )


    )
  )
)