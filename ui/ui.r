source('ui/competitionMatcher/competitionMatcher.r', local = TRUE)
source('ui/sidebar.r', local = TRUE)


ui <- dashboardPage(
  dashboardHeader(title = 'Better Brewery'),
  
  sidebar,
  
  dashboardBody(
    useShinyjs(),
    
    tabItems(

        competitionMatcher,

        tabItem(tabName = 'regionAnalyzer',
          box(tags$p('This is text')))

      )

  )
)