library(tidyverse)

group <- read.csv('result_laptop.csv')
random <- read.csv('result_desktop.csv')
random$id <- rep(1:50, each = 10)


group_summary <- group %>% 
  group_by(id) %>% 
  summarize(lat_mean = mean(output_lat), lon_mean = mean(output_lon)) %>% 
  inner_join(group) %>% 
  mutate(deviation = ((output_lat - lat_mean)^2 + (output_lon - lon_mean)^2)) %>% 
  group_by(id) %>% 
  summarize(sse = sum(deviation))

group %>% 
  filter(id > 505 & id < 513) %>% 
  ggplot(aes(x = output_lon, y = output_lat, group = factor(id))) +
  geom_jitter(aes(color = factor(id), shape = factor(id)), width = .5, height = .5, size = 2)


random_summary <- random %>% 
  group_by(id) %>% 
  summarize(lat_mean = mean(output_lat), lon_mean = mean(output_lon)) %>% 
  inner_join(random) %>% 
  mutate(deviation = ((output_lat - lat_mean)^2 + (output_lon - lon_mean)^2)) %>% 
  group_by(id) %>% 
  summarize(sse = sum(deviation))

random %>% 
  filter(id > 5 & id < 13) %>% 
  ggplot(aes(x = output_lon, y = output_lat, group = factor(id))) +
  geom_jitter(aes(color = factor(id), shape = factor(id)), height = 0.5, width = 0.5, size = 2)


random_summary$group <- 'Random'
group_summary$group <- 'Grouped'
summary_data <- rbind(random_summary, group_summary)

summary_data %>% 
  group_by(group) %>% 
  summarize(mse = mean(sse), sd = sd(sse)) %>% 
  ggplot(aes(x = group, y = mse)) +
  geom_bar(stat = 'identity') + 
  geom_errorbar(aes(ymin = mse - sd, ymax = mse + sd), width = 0.5) + 
  ylim(0, 4000) + 
  labs(
    y = 'Mean Squared Error',
    x = '',
    caption = 'Bars reflect standard deviations.'
  ) + 
  theme_bw() + 
  theme(text = element_text(size = 20))

ggsave('matcher_validation.png', height = 720 / 96, width = 1280 / 96, units = 'in')



