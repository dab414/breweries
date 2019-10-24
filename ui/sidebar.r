sidebar <- dashboardSidebar(
    sidebarMenu(
      menuItem('Competition Matcher', tabName = 'competitionMatcher', icon = icon('dashboard')),
      menuItem('Competition Analyzer', tabName = 'competitionAnalyzer', icon = icon('user', lib = 'glyphicon'))
    )
  )