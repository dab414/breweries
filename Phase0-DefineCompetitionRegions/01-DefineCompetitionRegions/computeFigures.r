library(tidyverse)
library(ggmap)
library(stats)
library(ggforce)

usa <- c(-125.771484,23.725012,-66.269531,49.239121)
usa_lat <- c(usa[2], usa[4])
usa_lon <- c(usa[1], usa[3])

# nj <- c(-76.102295,38.814031,-71.850586,41.438608)
# vermont <- c(-73.729248,42.698586,-71.773682,45.081279)
# colorado <- c(-109.094238,36.967449,-101.986084,41.021355)

d <- read.csv('../data/breweries.csv')

usa_map <- get_stamenmap(bbox = usa, zoom = 5, maptype = 'toner')

# nj_map <- get_stamenmap(bbox = nj, zoom = 10, maptype = 'toner')
# vermont_map <- get_stamenmap(bbox = vermont, zoom = 10, maptype = 'toner')
# colorado_map <- get_stamenmap(bbox = colorado, zoom = 8, maptype = 'toner')

ggmap(usa_map) +
  geom_point(data = d, aes(x = longitude, y = latitude), color = 'red', size = 0.5) +
  theme(axis.title = element_blank(),
        axis.ticks = element_blank(),
        axis.text = element_blank())

ggsave('00-justBreweries.png', width = 1280/96, height = 720/96, units = 'in')




#### CLUSTER THE BREWERIES BY LOCATION ####

d <- d[complete.cases(d),]

lat_filter <- (d$latitude > usa_lat[1]) & (d$latitude < usa_lat[2]) 
lon_filter <- (d$longitude > usa_lon[1]) & (d$longitude < usa_lon[2]) 

d <- d[lat_filter & lon_filter,]
d <- d[d$brewery_type == 'micro', ]

km <- kmeans(d[,c('latitude', 'longitude')], centers = 150)

centers <- data.frame(km$centers)
centers$label <- row.names(centers)

d$cluster <- factor(km$cluster)

centers <- d %>% 
  rename(label = cluster) %>% 
  group_by(label) %>% 
  summarize(count = n()) %>% 
  inner_join(centers, by = c('label'))


ggmap(usa_map) +
  #geom_circle(data = centers, aes(x0 = lon, y0 = lat, r = count, color = label), alpha = .5) + ## NOT WORKING
  geom_point(data = d, aes(x = longitude, y = latitude, color = cluster), size = .5) +
  theme(legend.position = 'None',
        axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank()) 
  #geom_point(data = data.frame(km$centers), aes(x = longitude, y = latitude, color = cluster), alpha = .3)

ggsave('01-ClusteredBreweries.png', width = 1280/96, height = 720/96, units = 'in')



#### FOCUS ON SIMILAR COMPETITION SPHERES ####

## im just gonna choose three randomly for now

set.seed(413)
random_user_location <- data.frame(longitude = runif(1, usa[1], usa[3]), latitude = runif(1, usa[2], usa[4]))
set.seed(555)
chosen_centers <- centers[sample(nrow(centers), 3),]

## individual
ggmap(usa_map) +
  geom_point(data = random_user_location, aes(x = longitude, y = latitude), size = 4, shape = 23, fill = 'green') +
  theme(axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank()) 
ggsave('02-JustIndividual.png', width = 1280/96, height = 720/96, units = 'in')

## target region
ggmap(usa_map) +
  geom_point(data = random_user_location, aes(x = longitude, y = latitude), size = 7, color = 'green', alpha = .6) +
  theme(axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank()) 
ggsave('03-JustTargetRegion.png', width = 1280/96, height = 720/96, units = 'in')

## matching competitve spheres
ggmap(usa_map) +
  geom_point(data = random_user_location, aes(x = longitude, y = latitude), size = 7, color = 'green', alpha = .6) +
  geom_point(data = chosen_centers, aes(x = longitude, y = latitude), size = 7, color = 'blue', alpha = .6) +
  theme(axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank()) 
ggsave('04-CompetitionSpheres.png', width = 1280/96, height = 720/96, units = 'in')

## hone in on one spot

highlighted_area <- d %>% 
  filter(cluster == 56) 

bb_highlight <- c(min(highlighted_area$longitude), min(highlighted_area$latitude), max(highlighted_area$longitude), max(highlighted_area$latitude))  
buffer <- .5
bb_modulate <- c(-1, -1, 1, 1)
bb_modulate <- bb_modulate * buffer

bb_highlight <- bb_highlight + bb_modulate

highlight_map <- get_stamenmap(bb = bb_highlight, zoom = 9, maptype = 'toner')


ggmap(highlight_map) + 
  geom_point(data = highlighted_area, aes(x = longitude, y = latitude), size = 3, color = 'blue') +
  theme(axis.title = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank()) 
  

ggsave('05-OneCompetitionSphere.png', width = 1280/96, height = 720/96, units = 'in')










#### DETERMINING BEST K VALUE #####

result <- data.frame(k = numeric(), cluster = numeric(), count = numeric(), miles_dev = numeric())

for (i in seq(100,500, 50)){
  
  km <- kmeans(d[,c('latitude', 'longitude')], centers = i)
  
  d$cluster <- factor(km$cluster)
  
  out <- d %>% 
    group_by(cluster) %>% 
    summarize(count = n()) 
  
  
  result <- rbind(result, data.frame(k = rep(i, nrow(out)), cluster = out$cluster, count = out$count, miles_dev = sqrt(km$withinss / i) * 69))
}

head(result)

result %>% 
  mutate(cluster = factor(cluster)) %>% 
  ggplot(aes(x = miles_dev)) +
  geom_histogram(color = 'black') +
  facet_wrap(~k)

result %>% 
  filter(k < 400) %>% 
  ggplot(aes(x = miles_dev, y = count)) +
  geom_hline(yintercept = 5, linetype = 'dashed') +
  geom_point() +
  facet_wrap(~k) +
  scale_x_continuous(labels = seq(0, 100, 10), breaks = seq(0, 100, 10))




d %>% 
  group_by(cluster) %>% 
  summarize(count = n()) %>% 
  ggplot(aes(x = count)) +
  geom_histogram(color = 'black')








