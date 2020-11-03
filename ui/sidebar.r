sidebar <- dashboardSidebar(
    sidebarMenu(
    	id = 'tabs',
      menuItem('Competition Matcher', tabName = 'competitionMatcher', icon = icon('dashboard')),
      menuItem('Competition Analyzer', tabName = 'competitionAnalyzer', icon = icon('user', lib = 'glyphicon')),
      menuItem('About', tabName = 'about', icon = icon('info-sign', lib = 'glyphicon'))
    )
  )