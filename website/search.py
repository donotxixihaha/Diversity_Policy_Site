from django.db import connection
from .models import Policy

# currently gets 100 results--will need to figure out a way to get best number of potentially useful results
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
 

    STMT = "SELECT title, school, department, administrator, author, " + \
                  "state, city, latitude, longitude, link, " + \
                  "(CASE WHEN published_date < '1000-01-01' THEN NULL " + \
                        "ELSE published_date " + \
                   "END) AS published_date, " + \
                  "tags, abstract, text " + \
           "FROM policies " + \
           "WHERE " + STMT_FILTER + \
                  "title LIKE \'%" + query + "%\' OR " + \
                  "abstract LIKE \'%" + query + "%\';"

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
    results = policies.query.msearch(query)
    db.session.remove()
    return results
