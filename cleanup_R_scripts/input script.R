library(magrittr)
library(dplyr)
library(ggplot2)
library(tidyr)
library(stringr)

#decision tree to ensure different platforms can easily run the data
if(Sys.info()["user"] == "dark_") {
  PROJECTDIR <- file.path("C:", "Users", "dark_","OneDrive", "Documents", "db_cleanup")
  fileName <- "raw_db.csv"
  
} #add an else if for extra users

setwd(PROJECTDIR)

#reads in the db, titling the columns appropriately
data <- read.csv(fileName, col.names = c('id', #done
                                         'timestamp', #done
                                         'title', 
                                         'school', #done
                                         'department', #done
                                         'administrator', #done
                                         'author', #done
                                         'state', #done
                                         'city', #done
                                         'latitude', #done
                                         'longitude', #done 
                                         'link', #done 
                                         'published_date', 
                                         'tags', #done 
                                         'abstract', #done
                                         'text') #done
                          , stringsAsFactors = F
                          , encoding = "UTF-8")

