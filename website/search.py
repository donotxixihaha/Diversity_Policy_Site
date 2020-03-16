from django.db import connection
from .models import Policy


# Return a sql statement to find records with pattern of a sequence of words,
# if the given sequence term list is non-empty, otherwise return an empty string.
#
# @param field - a string of field name
# @param seq_term - a list of a sequence of words
# @return seq_pattern - a string of sql statement
#
# sql statement format: 
# field LIKE '%seq_term[0]%seq_term[1]%seq_term[2]%...%seq_term[end]%'
#
def get_seq_stmt(field, seq_term):

    if seq_term:
        seq_pattern = field + " LIKE \'%"
        for i in seq_term:
            seq_pattern += i + "%"
        seq_pattern += "\'"
        return "(" + seq_pattern + ")"
    else:
        return ""


# Return a sql statement to find records with exact match of 
# a list of phrases and words,
# if the given exact term set or include term list is non-empty, 
# otherwise return an empty string.
#
# @param field - a string of field name
# @param exact_term - a list of phrases or words to exact match
# @return exact_pattern - a string of sql statement
#
# sql statement format: 
# field LIKE '%exact_term[0]%' OR 
# field LIKE '%exact_term[1]%' OR ... OR 
# field LIKE '%exact_term[end]%'
#
def get_exact_stmt(field, exact_term):

    if exact_term:
        exact_pattern = ""
        for i in range(len(exact_term)):
            exact_pattern += field + " LIKE \'%" + exact_term[i] + "%\'"
            if i < len(exact_term) - 1:  # not the last one
                exact_pattern += " OR "
        return "(" + exact_pattern + ")"
    else:
        return ""


# Return a sql statement to find records without a list of words,
# if the given exclude term list is non-empty, 
# otherwise return an empty string.
#
# @param field - a string of field name
# @param exclude - a list of words to exclusive match
# @return exclude_pattern - a string of sql statement
#
# sql statement format: 
# field NOT LIKE '%exclude_term[0]%' AND 
# field NOT LIKE '%exclude_term[1]%' AND ... AND 
# field NOT LIKE '%exclude_term[end]%'
#
def get_exclude_stmt(field, exclude_term):
    
    if exclude_term:
        exclude_pattern = ""
        for i in range(len(exclude_term)):
            exclude_pattern += field + " NOT LIKE \'%" + exclude_term[i] + "%\'"
            if i < len(exclude_term) - 1:  # not the last one
                exclude_pattern += " AND "
        return "(" + exclude_pattern + ")"
    else:
        return ""


# Return sql statement of searching terms, with the given type and terms search,
# if the given type is valid,
# otherwise return an empty string
#
# @param stmt_term - a sql statement string
# @param type_name - a string represents search type
# @param terms - a list of terms to search
# @return stmt_term - a sql statement
#
def get_stmt_term(stmt_term, type_name, terms):
    FIELDS = ('title', 'school', 'department', 'administrator', 'author',
              'state', 'city', 'link', 'tags', 'abstract')
    TYPES = ('seq', 'exact', 'exclude')

    if type_name not in TYPES:
        return ""

    for field in FIELDS:
        if type_name == TYPES[0]:
            seq_term = terms
            cur_stmt = get_seq_stmt(field, seq_term)
        elif type_name == TYPES[1]:
            exact_term = terms
            cur_stmt = get_exact_stmt(field, exact_term)
        else:  # TYPES[2]
            exclude_term = terms
            cur_stmt = get_exclude_stmt(field, exclude_term)
        if cur_stmt:
            if stmt_term:  # non-empty stmt, need prepend ADD
                if type_name == TYPES[2]:
                    stmt_term += " AND "
                else:
                    stmt_term += " OR "
            stmt_term += cur_stmt
    return stmt_term

# Return sql statement of filter terms, inclusive search.
#
# @param filters - a set of filter terms
# @return stmt_term - a sql statement
#
def get_stmt_filter(filters):

    stmt = "("
    first_flag = True
    for i in filters:
        if first_flag:
            first_flag = False
        else:
            stmt += " OR "
        stmt += i
    return stmt + ")"

# Search the policies in the database with the matching requirements.
#
# @param query - search term expression
# @param filter - filter term list
# @return result - a list of policy objects matched with the given query and filter
#
def search(query, filter=None):
    
    SPLITTER = ("\"", "-", "[", "]")

    STMT_FILTER = ""

    schools = set()
    states = set()
    years = set()
    if filter:
        for i in filter:
            if i.isnumeric():  # date filter
                start_of_yr = i + "-01-01"
                end_of_yr = i + "-12-31"
                yr = "(published_date <= \'" + end_of_yr + "\' AND " + \
                     "published_date >= \'" + start_of_yr + "\')"
                years.add(yr)
            elif "-state" in i:  # state filter
                state = "state = \'" + i.replace("-state", "") + "\'"
                states.add(state)
            else:  # school filter
                school = "school = \'" + i + "\'"
                schools.add(school)
    if schools:
        STMT_FILTER += get_stmt_filter(schools)
    if states:
        if schools:
            STMT_FILTER += " AND "
        STMT_FILTER += get_stmt_filter(states)
    if years:
        if schools or states:
            STMT_FILTER += " AND "
        STMT_FILTER += get_stmt_filter(years)

    if STMT_FILTER:
        STMT_FILTER += " AND "

    # print(STMT_FILTER)
    seq_term = []
    exact_term = set()
    exclude_term = set()
    
    # exact phrase search, # quotes should be even,
    # otherwise take it as inclusive pattern
    if SPLITTER[0] in query and query.count(SPLITTER[0]) % 2 == 0:
        exact_flag = False
        start_idx = -1
        end_idx = -1

        i = 0
        while i < len(query):
            if not exact_flag and query[i] == SPLITTER[0]:
                start_idx = i
                exact_flag = True   
            elif exact_flag and query[i] == SPLITTER[0]:
                end_idx = i
                exact_term.add(query[start_idx+1:end_idx])
                exact_flag = False
                query = query[:start_idx] + " " + query[end_idx+1:]
                i = start_idx - 1
            i += 1

    query = query.strip(" ") + " "
    # print(query)

    # exlusive word search
    if SPLITTER[1] in query:
        exclude_flag = False
        start_idx = -1
        end_idx = -1

        i = 0
        while i < len(query):
            if not exclude_flag and query[i] == SPLITTER[1]:
                start_idx = i
                exclude_flag = True        
            elif exclude_flag and query[i] == ' ':
                end_idx = i
                exclude_term.add(query[start_idx+1:end_idx])
                exclude_flag = False
                query = query[:start_idx] + " " + query[end_idx+1:]
                i = start_idx - 1
            i += 1

    query = query.strip(" ")
    # print(query)

    # a sequence of words search, square brackets should be paired,
    # otherwise take it as inclusive pattern
    if SPLITTER[2] in query and SPLITTER[3] in query:
        seq_flag = False
        start_idx = -1
        end_idx = -1

        i = 0
        while i < len(query):
            if query[i] == SPLITTER[2]:
                start_idx = i
                seq_flag = True
            elif query[i] == SPLITTER[3]:
                end_idx = i
                seq_term.extend(query[start_idx+1:end_idx].split(" "))
                seq_flag = False
                query = query[:start_idx] + " " + query[end_idx+1:]
                i = start_idx - 1
            i += 1
    
    for i in SPLITTER:
        query = query.replace(i, "")
    query = query.strip(" ")
    include_term = set()
    if query:
        include_term = set(query.split(" "))
        

    # print("seq    :", seq_term)
    # print("exact  :", list(exact_term))
    # print("include:", list(include_term))
    # print("exclude:", list(exclude_term))
    
    if include_term:
        exact_term = exact_term.union(include_term)

    STMT_TERM = ""
    STMT_TERM = get_stmt_term(STMT_TERM, "seq", seq_term)
    STMT_TERM = get_stmt_term(STMT_TERM, "exact", list(exact_term))
    STMT_TERM = get_stmt_term(STMT_TERM, "exclude", list(exclude_term))
  
    STMT = "SELECT title, school, department, administrator, author, " + \
                  "state, city, link, " + \
                  "(CASE WHEN published_date < '1000-01-01' THEN NULL " + \
                        "ELSE published_date " + \
                   "END) AS published_date, " + \
                  "tags, abstract " + \
           "FROM policies " + \
           "WHERE " + STMT_FILTER + "(" + STMT_TERM + ");"

    # print(STMT)
    print("START Fetching...")
    result = []
    with connection.cursor() as cursor:
        cursor.execute(STMT)
        rows = cursor.fetchall()
        for row in rows:
            item = Policy(
                title = row[0],
                school = row[1],
                department = str(row[2] or ''),
                administrator = str(row[3] or ''),
                author = str(row[4] or ''),
                state = row[5],
                city = row[6],
                latitude = "",
                longitude = "",
                link = row[7],
                published_date = row[8],
                tags = str(row[9] or ''),
                abstract = str(row[10] or ''),
                text = ""
            )
            result.append(item)
    print("END Fetching.")
    print("length of result:", len(result))
    return result

# Functions similarly to search(), except results are found using prefix, only searching over title field, and object
# is used differently than the search() object is in the function calling search_suggest()

def search_suggest(query):
    # results = policies.query.msearch(query)
    # db.session.remove()
    return []
