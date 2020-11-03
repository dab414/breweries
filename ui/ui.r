source('ui/competitionMatcher/competitionMatcher.r', local = TRUE)
source('ui/sidebar.r', local = TRUE)
source('ui/competitionAnalyzer/competitionAnalyzer.r', local = TRUE)
source('ui/about/about.r', local = TRUE)


ui <- dashboardPage(
  
  dashboardHeader(title = 'Better Brewery'),

  sidebar,
  
  dashboardBody(id = 'main_tabs',
    tags$script(HTML('$("body").addClass("sidebar-mini");')),
    useShinyjs(),
    
    tabItems(

        competitionMatcher,

        competitionAnalyzer,

        about

      )

  )
)