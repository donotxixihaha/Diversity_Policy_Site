source('input script.R')


states_unique <-
  data %>% 
  #excess white spaces accounts for 53 of the extra values
  mutate(state = trimws(state)) %>% 
  
  #improper case accounts for 4 of the extra values
  mutate(state = tolower(state)) %>% 
  
  #Removing non word characters only accounts for 1 of the extra values
  #mutate(state = str_remove_all(state, "\\W")) %>% 
  group_by(state) %>% 
  summarise(count = n()) 

data <-
  data %>% 
  filter(!(state == '' & city == '' & abstract == '' & text == ''))


city_unique <-
  data %>% 
  #104 out of 423 are a product of excess whitespace
  mutate(city = trimws(city)) %>% 
  #24 of 423 are a product of case errors
  mutate(city = tolower(city)) %>% 
  group_by(city) %>% 
  summarise(count = n()) %>%
  arrange(count)
  
  
school_unique <-
  data %>% 
  #121 out of 497 are a product of excess whitespace
  mutate(school = trimws(school)) %>% 
  #20 out of 497  are a product of case errors
  mutate(school = tolower(school)) %>% 
  group_by(school) %>% 
  summarise(count = n()) %>% 
  arrange(count)


lat <-
  data %>% 
  group_by(latitude) %>% 
  summarise(count = n()) %>% 
  arrange(count)

long <-
  data %>% 
  #mutate(longitude = str_remove_all(longitude, '\\W')) %>% 
  group_by(longitude) %>% 
  summarise(count = n()) %>% 
  arrange(count)
  
department <-
  data %>% 
  mutate(department = trimws(department)) %>% 
  mutate(department = tolower(department)) %>% 
  mutate(department = str_remove_all(department, '\\W')) %>% 
  group_by(department) %>% 
  summarise(count = n()) %>% 
  arrange(count)

department %>% 
  filter(count <= 1) %>% 
  count()
  summarise(sum(count))

department %>% 
  tail(10) %>% 
  summarise(sum(count))

ggplot(data = department %>% filter(department != '')) +
  aes(x = count) +
  geom_histogram(binwidth = 1)

ggplot(data = department %>% 
                filter(department != '') %>% 
                filter(count < 500)) +
  aes(x = count) +
  geom_histogram(binwidth = 1)


author <-
  data %>% 
  mutate(author = trimws(author)) %>% 
  mutate(author = tolower(author)) %>% 
  mutate(author = str_remove_all(author, '\\W')) %>% 
  group_by(author) %>% 
  summarise(count = n()) %>% 
  arrange(count)

administrator <-
  data %>% 
  mutate(administrator = trimws(administrator)) %>% 
  mutate(administrator = tolower(administrator)) %>% 
  mutate(administrator = str_remove_all(administrator, '\\W')) %>% 
  group_by(administrator) %>% 
  summarise(count = n()) %>% 
  arrange(count)

link <-
  data %>% 
  mutate(link = trimws(link)) %>% 
  mutate(link = tolower(link)) %>% 
  group_by(link) %>% 
  summarise(count = n()) %>% 
  arrange(count)

sub_link <-
  link %>% 
  #slices the link to just the first 3 letters
  mutate(link = str_sub(link, 1, 4)) %>% 
  group_by(link) %>% 
  summarise(count = n()) %>% 
  arrange(count)

sub_link %>% 
  filter(link != 'http') %>% 
  filter(link != 'file') %>% 
  summarise(sum(count))

link %>% filter(str_sub(link, 1, 4) == 'file')


tags <-
  data %>% 
  mutate(tags = trimws(tags)) %>% 
  mutate(tags = tolower(tags)) %>% 
  #slices the tags to just the first 5 letters
  mutate(tags = str_sub(tags, 1, 6)) %>% 
  group_by(tags) %>% 
  summarise(count = n()) %>% 
  arrange(count)

abstract <-
  data %>% 
  mutate(abstract = trimws(abstract)) %>% 
  mutate(abstract = tolower(abstract)) %>% 
  group_by(abstract) %>% 
  summarise(count = n()) %>% 
  arrange(count)

text <-
  data %>% 
  mutate(text = trimws(text)) %>% 
  mutate(text = tolower(text)) %>% 
  group_by(text) %>% 
  summarise(count = n()) %>% 
  arrange(count)

id <-
  data %>% 
  mutate(id = trimws(id)) %>% 
  mutate(id = tolower(id)) %>% 
  group_by(id) %>% 
  summarise(count = n()) %>% 
  arrange(count)

alpha_id <-
  data %>% 
  #entries that are strictly numbers will get reduced to blank string
  mutate(id = str_remove_all(id, '\\d')) %>% 
  filter(id != '')
         
timestamp <-
  data %>% 
  mutate(timestamp = trimws(timestamp)) %>% 
  mutate(timestamp = tolower(timestamp)) %>% 
  group_by(timestamp) %>% 
  summarise(count = n()) %>% 
  arrange(count)

digits_timestamp <-
  data %>% 
  #entries that are strictly numbers will get reduced to blank string
  mutate(timestamp = str_remove_all(timestamp, '\\d')) %>% 
  group_by(timestamp) %>% 
  summarise(count = n()) %>% 
  arrange(count)

titles <-
  data %>% 
  group_by(title) %>% 
  summarise(count = n()) %>% 
  arrange(count)
