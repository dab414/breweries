source('ui/competitionMatcher/summaryBox.r', local = TRUE)
source('ui/competitionMatcher/mapBox.r', local = TRUE)

competitionMatcher <- tabItem(
  tabName = 'competitionMatcher', 
  mapBox,
  summaryBox
  )