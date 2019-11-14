about <- tabItem(
  tabName = 'about',
  box(width = 12,
    h2('About'),
    h3('Data sources'),
    p('There were many different data sources used for this project. The main data sources that were relied upon for matching user zip codes to existing competition areas were tap water data and census data. A wider variety of data was scraped for analyzing trends within a competition area, and perhaps the most notable source was ratebeer.com. The full sources are listed below:'),
    tags$b('Matching user zip codes to breweries:'),
    tags$ul(
      tags$li(tags$a(href='https://ewg.org', 'EWG')),
      tags$li(tags$a(href='https://factfinder.census.gov', 'Census.gov'))
    ),
    tags$b('Analyzing competition areas:'),
    tags$ul(
      tags$li(tags$a(href='https://ratebeer.com', 'Ratebeer')),
      tags$li(tags$a(href='https://untappd.com', 'Untappd')),
      tags$li(tags$a(href='https://twitter.com', 'Twitter')),
      tags$li(tags$a(href='https://yelp.com', 'Yelp'))
    ),

    h3('Algorithms'),
    p('The first notable algorithm that was used was K-Means clustering to establish the competition areas. This was done by first collecting the latitude and longitude for each brewery in the US and then doing a simple, two-dimensional clustering on their coordinates. I settled on around 150 clusters because this number allowed for at least five breweries per cluster and most clusters had a physical radius of 50 miles or fewer. These features were important because these clusters were meant to represent competition areas, and so we would want at least five breweries to be competing with each other and we want those breweries to be in close enough proximities where it would make sense that they were competing with one another.'),
    p("The next notable algorithm was the one that was used to identify similar competition regions for a given user zip code. This algorithm was similar to clustering, in that the goal was to find which competition areas were nearest to the user's location in terms of feature space. For each competition area, roughly 100 features were computed that represented both the contaminants in the tap water as well as demographic information for that given region. Once a user inputs a zipcode, these same features tap water and demographic features were then computed for a user's zipcode in realtime. The Euclidean distance was computed between the user's feature vector and each competition region, and the competition areas with the smallest three distances were selected as being the areas that were most similar to the user's area."),

    h3('Business Objective'),
    p("The business objective of Better Brewery is to provide a service for people who either own their own brewery or are looking to open their own brewery. Brewing beer has become increasingly popular over the last several decades, which means that there's a great deal of competition for those who are looking to get into the beer brewing business. My app is intended to make opening a brewery feel less overwhelming by giving prospective brewery owners an easy place to start."),
    p("The first step is to analyze the area that the user is looking to open a brewery and find other areas in the country that are similar in terms of their preconditions for brewery success. An example of what I mean by preconditions for success is something like tap water. Tap water is essential for brewing beer, and it's something about an area that cannot be changed. If I'm able to find areas that have similar tap water compared to our user's location, I can look to see how other breweries have been successful given that same tap water, and then make recommendations to the user about what strategies might be successful."),
    p("The current iteration of Better Brewery (11-13-2019) matches a user's location to similar location by analyzing tap water contaminants and demographic characteristcs. Once a user selects a similar region to analyze, the app simply presents the top rated beers in that competition area, as well as a review of the top rated beer. Choosing which beers to brew is often one of the first things that a new brewery owner needs to decide on. Presenting information on the top-performing beers is meant to give a user an easy place to start by suggesting which beers to brew first. The user can begin brewing these beers and trust that he or she is well on the way to building a better brewery.")

  )
)