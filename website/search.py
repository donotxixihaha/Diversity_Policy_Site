from django.db import connection
from .models import Policy


# Search the policies in the database with the matching requirements.
#
# @param query - search term expression
# @param filter - filter term list
# @return result - a list of policy objects matched with the given query and filter
#
def search(query, filter=None):

    STMT_FILTER = ''

    if filter:
        first_flag = True
        for i in filter:
            if first_flag:
                first_flag = False
            else:
                STMT_FILTER += " OR "

            if i.isnumeric():
                start_of_yr = i + "-01-01"
                end_of_yr = i + "-12-31"
                STMT_FILTER += "published_date <= \'" + end_of_yr + "\' AND " + \
                               "published_date >= \'" + start_of_yr + "\'"
            else:
                STMT_FILTER += "school = \'" + i + "\'"
        STMT_FILTER += " AND "
 
    SPLITTER = ("\"", "-", "[", "]")

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
    
    include_term = set(query.strip(" ").split(" "))

    # print("seq    :", seq_term)
    # print("exact  :", list(exact_term))
    # print("include:", list(include_term))
    # print("exclude:", list(exclude_term))
 

    STMT_TERM = ""

    # abstract LIKE '%seq_term[0]%seq_term[1]%seq_term[2]%...%seq_term[end]%'
    if seq_term:
        seq_pattern = "abstract LIKE \'%"
        for i in seq_term:
            seq_pattern += "" + i + "%"
        seq_pattern += "\'"
        STMT_TERM += "(" + seq_pattern + ")"

    # abstract LIKE '%exact_term[0]%' OR 
    # abstract LIKE '%exact_term[1]%' OR ...  OR 
    # abstract LIKE '%exact_term[end]%'
    exact_term = exact_term.union(include_term)
    if exact_term:
        exact_pattern = "abstract LIKE \'%"
        for i in exact_term:
            exact_pattern += i + "%\' OR abstract LIKE \'%"
        exact_pattern = exact_pattern.rstrip("\' OR abstract LIKE \'%")
        exact_pattern += "\'"
        if seq_term:
            STMT_TERM += " AND "
        STMT_TERM += "(" + exact_pattern + ")"

    # abstract NOT LIKE '%exclude_term[0]%' AND 
    # abstract NOT LIKE '%exclude_term[1]%' AND ...  AND 
    # abstract NOT LIKE '%exclude_term[end]%'
    if exclude_term:
        print("hhhh", exclude_term)
        exclude_pattern = "abstract NOT LIKE \'%"
        for i in exclude_term:
            exclude_pattern += i + "%\' AND abstract NOT LIKE \'%"
        print("before:", exclude_pattern)
        exclude_pattern = exclude_pattern.rstrip(" abstract NOT LIKE \'%")
        exclude_pattern = exclude_pattern.rstrip("\' AND")
        print("after :", exclude_pattern)
        exclude_pattern += "\'"
        if exact_term:
            STMT_TERM += " AND "
        STMT_TERM += "(" + exclude_pattern + ")"
  
    

    STMT = "SELECT title, school, department, administrator, author, " + \
                  "state, city, latitude, longitude, link, " + \
                  "(CASE WHEN published_date < '1000-01-01' THEN NULL " + \
                        "ELSE published_date " + \
                   "END) AS published_date, " + \
                  "tags, abstract, text " + \
           "FROM policies " + \
           "WHERE " + STMT_FILTER + STMT_TERM + ";"

    print(STMT)
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
                latitude = row[7],
                longitude = row[8],
                link = row[9],
                published_date = row[10],
                tags = str(row[11] or ''),
                abstract = str(row[12] or ''),
                text = str(row[13] or '')
            )
            result.append(item)
    print("END Fetching.")
    print("length of result:", len(result))
    return result

    # results = policies.query.msearch(query)
    # db.session.remove()
    # if(filter==None or len(filter)==0):
    #     return results
    # years = []
    # schools = []
    # for f in filter:
    #     if(f[0].isdigit()):
    #         years.append(f)
    #     else:
    #         schools.append(f)
    # if(years==None or len(years)==0):
    #     return results.filter(policies.school.in_(schools))
    # elif(schools==None or len(schools)==0):
    #     results = results.filter(extract('year', policies.published_date).in_(years))
    #     return results
    # else:
    #     return results.filter((policies.school.in_(schools)&extract('year', policies.published_date).in_(years)))

# Functions similarly to search(), except results are found using prefix, only searching over title field, and object
# is used differently than the search() object is in the function calling search_suggest()

def search_suggest(query):
    # results = policies.query.msearch(query)
    # db.session.remove()
    return []
