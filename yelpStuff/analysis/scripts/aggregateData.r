## This script takes in all the data files from Yelp and compiles them to one csv

library(tidyverse)

f <- list.files('../../scrape/exportData/finalData/')

count <- 0

holder <- list()

for (e in f) {
  count <- count + 1
  holder[[count]] <- read.csv(paste('../../scrape/exportData/finalData/', e, sep=''))
  #nam <- paste('df', count, sep='')
  #assign(nam, read.csv(paste('../../exportData/finalData/', e, sep='')))
}

count <- 0
for (e in holder){
  count <- count + 1
  if ('X' %in% colnames(e)) {
    holder[[count]] <- e %>% 
      select(-X)
  }
}

for (e in holder){
  print(ncol(e))
}

outData <- holder[[1]]

for (e in 2:(length(holder))){
  outData <- rbind(outData, holder[[e]])
}

write.csv(outData, '../data/yelpData.csv', row.names = FALSE)
