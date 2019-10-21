sidebar <- dashboardSidebar(
    sidebarMenu(
      menuItem('Competition Matcher', tabName = 'competitionMatcher', icon = icon('dashboard')),
      menuItem('Region Analyzer', tabName = 'regionAnalyzer', icon = icon('user', lib = 'glyphicon'))
    )
  )