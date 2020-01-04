source('input script.R')

#removes the approximately 250 blank entries
data <-
  data %>% 
  filter(!(state == '' & city == '' & abstract == '' & text == ''))

alpha_id <-
  data %>% 
  #entries that are strictly numbers will get reduced to blank string
  mutate(id = str_remove_all(id, '\\d')) %>% 
  #removes the blank strings(valid ID values)
  filter(id != '') %>% 
  #removes the 19th entry, which is an otherwise valid row of data
  slice(1:18) %>% 
  #retains only the ID column for later membership test
  select(id)

#Removes the 18 "nonsense" rows
data <-
  data %>% 
  #memberhsip test: removes any rows that share a ID value alpha_id
  filter(!(is.element(id, alpha_id$id)))

remove(alpha_id)

#Suggest sending the below data to Omar, along with the list of tag options, 
#and then manually adding the tags Omar suggests. 
#missing_tags <-
#  data %>% 
#  filter(tags  == '')

city_state <-
  #inputs the downloaded states and city data set
  read.csv('uscities.csv', stringsAsFactors = F) %>% 
  select(city_ascii, state_name) %>% #be sure to use city_ascii not of city
  #converts to lower case to ensure compatability 
  mutate(city_ascii = tolower(city_ascii)) %>% 
  mutate(state_name = tolower(state_name))

data <-
  data %>% 
  #whitespace and case removal for State column
  mutate(state = trimws(state)) %>% 
  mutate(state = tolower(state)) %>% 
  #whitespace and case removal for City column
  mutate(city = trimws(city)) %>% 
  mutate(city = tolower(city)) %>% 
  #whitespace and case removal for School column
  mutate(school = trimws(school)) %>% 
  mutate(school = tolower(school))

#creates a summary of all State values that do not conform.
state_errors <-
  data %>% 
  filter(!(is.element(state, city_state$state_name ))) %>% 
  group_by(state) %>% 
  summarise(count = n()) %>% 
  arrange(count)

#creates a reference value for the 'new yorkâ ' value which did not seem to respond to copy and paste
n_y <-
  data %>% 
  filter(!(is.element(state, city_state$state_name ))) %>%
  mutate(state_short = str_sub(state, 1, 8)) %>% 
  filter(state_short == 'new york') %>% 
  group_by(state) %>% 
  summarise(n())

#replaces erroneous state values with correct ones
data <-
  data %>% 
  #taking the opportunity to fix the city value in the same row, before fixing the state
  mutate(city = replace(city, state == 'williamstown', 'williamstown')) %>% 
  mutate(city = replace(city, state == 'lexington', 'lexington')) %>%
  mutate(city = replace(city, state == 'claremont', 'claremont')) %>% 
  mutate(city = replace(city, state == '30.6919', 'Mobile')) %>% 
  mutate(city = replace(city, state == 'columbia', 'columbia')) %>% 
  mutate(city = replace(city, state == 'milwaukee', 'milwaukee')) %>% 
  mutate(city = replace(city, state == 'madison', 'madison')) %>% 
  mutate(city = replace(city, is.element(state, c('church', 'presbyterian')), 'point lookout')) %>% 
  mutate(city = replace(city, state == 'norman', 'norman')) %>% 
  mutate(city = replace(city, state == 'moscow', 'moscow')) %>% 
  mutate(city = replace(city, state == 'louisville', 'Stony Brook')) %>% 
  mutate(city = replace(city, state == 'hanover', 'hanover')) %>%
  
  #taking the opportunity to fix the school value in the same row, before fixing the state
  mutate(school = replace(school, state == 'concord', 'University of New Hampshire')) %>%
  mutate(school = replace(school, state == 'maineacquisition of real property', 'University of Maine')) %>%
  mutate(school = replace(school, state == 'madison', 'University of Wisconsin')) %>% 
  mutate(school = replace(school, state == 'milwaukee', 'Marquette University')) %>%
  
  #fixing state values
  mutate(state = replace(state, is.element(state, c('albamba','30.6919')) , 'alabama')) %>% 
  mutate(state = replace(state, state == 'ar', 'arkansas')) %>% 
  mutate(state = replace(state, is.element(state, c('califronia', 'califonria', 'claremont')), 'california')) %>% 
  mutate(state = replace(state, state == 'conneticut', 'connecticut')) %>% 
  mutate(state = replace(state, state == 'district of colombia', 'washington d.c.')) %>% 
  mutate(state = replace(state, is.element(state, c('orlando', 'floirda', 'floriad')), 'florida')) %>% 
  mutate(state = replace(state, state == 'moscow', 'idaho')) %>% 
  mutate(state = replace(state, is.element(state, c('illionois', 'illionis')), 'illinois')) %>%  
  mutate(state = replace(state, str_detect(state, 'indiana'), 'indiana')) %>% 
  mutate(state = replace(state, is.element(state, c('kentuck','lexington')), 'kentucky')) %>% 
  mutate(state = replace(state, state == 'louisana', 'louisiana')) %>%  
  mutate(state = replace(state, state == 'maineacquisition of real property', 'maine')) %>% 
  mutate(state = replace(state, state == 'md', 'maryland')) %>% 
  mutate(state = replace(state, is.element(state, c('massachusettes', 'massachussettes', 'williamstown', '')), 'massachusetts')) %>%  
  mutate(state = replace(state, state == 'michigan.', 'michigan')) %>%
  mutate(state = replace(state, state == 'university of st. thomas', 'minnesota')) %>% 
  mutate(state = replace(state, state == 'mississppi', 'mississippi')) %>% 
  mutate(state = replace(state, is.element(state, c('columbia', 'church', 'presbyterian')), 'missouri')) %>% 
  mutate(state = replace(state, is.element(state, c('hanover','concord')), 'new hampshire')) %>% 
  mutate(state = replace(state, is.element(state, c('new jerser', 'new jersery', 'new jersy')), 'new jersey')) %>% 
  mutate(state = replace(state, is.element(state, c(n_y$state, 'louisville')), 'new york')) %>%   
  mutate(state = replace(state, state == 'norman', 'oklahoma')) %>% 
  mutate(state = replace(state, state == 'ri', 'rhode island')) %>%  
  mutate(state = replace(state, state == 'south carolian', 'south carolina')) %>% 
  mutate(state = replace(state, state == 'texcas', 'texas')) %>%   
  mutate(state = replace(state, state == 'vermotn', 'vermont')) %>% 
  mutate(state = replace(state, is.element(state, c('viriginia', 'va')), 'virginia')) %>% 
  mutate(state = replace(state, is.element(state, c('washinton', 'wa')), 'washington')) %>% 
  mutate(state = replace(state, is.element(state, c('milwaukee', 'marquette university', 'madison')), 'wisconsin'))

remove(n_y, state_errors)




#creates a summary of all City values that do not conform, rerun after cleaning to confim fix
errors <-
  data %>% 
  filter(!(is.element(city, city_state$city_ascii ))) %>% 
  group_by(city) %>% 
  summarise(count = n()) %>% 
  arrange(count)

 data <-
   data %>% 
   #fixing school names
   mutate(school = replace(school, city == 'colgate', 'colgate univeristy')) %>%  
   mutate(school = replace(school, city == 'villanova', 'villanova univeristy')) %>%  
   mutate(school = replace(school, str_detect(school, 'university of hawai'), 'university of hawaii')) %>%
   #fixing city names
   mutate(city = replace(city, city == 'melbourn', 'melbourne')) %>% 
   mutate(city = replace(city, city == 'saint paul', 'st. paul')) %>%
   mutate(city = replace(city, city == 'saint louis', 'st. louis')) %>% 
   mutate(city = replace(city, is.element(city, c('district of colombia', 'georgetown','washington')), 'washington d.c.')) %>% 
   mutate(city = replace(city, city == 'binghamton university - state university of new york', 'binghamton')) %>% 
   mutate(city = replace(city, city == 'bornx', 'bronx')) %>% 
   mutate(city = replace(city, city == 'colgate', 'hamilton')) %>%  
   mutate(city = replace(city, city == 'monroe county', 'rochester')) %>%  
   mutate(city = replace(city, city == 'new york city', 'new york')) %>% 
   mutate(city = replace(city, str_detect(city, 'bloomington'), 'bloomington')) %>% 
   mutate(city = replace(city, is.element(city, c('tuscan', 'tuscon')), 'tucson')) %>%   
   mutate(city = replace(city, city == 'lexington city', 'lexington')) %>% 
   mutate(city = replace(city, city == 'haverford college', 'haverford')) %>% 
   
   #arbitrary placement of tufts university in medford
   mutate(city = replace(city, school == 'tufts university', 'medford')) 
   #mutate(city = replace(city, city == 'villanova', 'Radnor Township')) %>% 

write.csv(data, file = 'updated_db.csv', fileEncoding ="UTF-8")

