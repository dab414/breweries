sidebar <- dashboardSidebar(
    sidebarMenu(
    	id = 'tabs',
      menuItem('Select Area', tabName = 'competitionMatcher', icon = icon('dashboard')),
      menuItem('See Breweries in Area', tabName = 'competitionAnalyzer', icon = icon('user', lib = 'glyphicon')),
      menuItem('About', tabName = 'about', icon = icon('info-sign', lib = 'glyphicon'))
    )
  )