from django.utils import timezone
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Policy
from .search import search, search_suggest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

import json
import ast

# Create your views here.
from django.core.paginator import Paginator, Page

class DSEPaginator(Paginator):
    """
    Override Django's built-in Paginator class to take in a count/total number of items;
    Elasticsearch provides the total as a part of the query results, so we can minimize hits.
    """
    def __init__(self, *args, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._count = self.object_list.hits.total

    def page(self, number):
        # this is overridden to prevent any slicing of the object_list - Elasticsearch has
        # returned the sliced data already.
        number = self.validate_number(number)
        return Page(self.object_list, number, self)

def search_home(request):
    return render(request, 'website/search_home.html')

def about_page(request):
    return render(request, 'website/about_page.html')

def contribute_policy(request):
    return render(request, 'website/contribute_policy.html')

def build_local_table():
    STMT = "SELECT title,\
                   school,\
                   department,\
                   administrator,\
                   author,\
                   state,\
                   city,\
                   latitude,\
                   longitude,\
                   link,\
                   (CASE \
                         WHEN published_date < '1000-01-01' THEN NULL \
                         ELSE published_date \
                    END) AS published_date,\
                   tags,\
                   abstract,\
                   text \
            FROM website_policy"
    print("START")
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
            item.save()
    print("END")

def policy_search(request):

    # if the table is empty, insert data from remote db
    items = Policy.objects.all()
    if len(items) == 0:
        build_local_table()


    # table_name = 'policies'
    # term_search_lst = ['title','school','abstract']
    term = request.GET.get('search')
    fil = request.GET.getlist('filter')

    # print(term, fil)
    policies = search(term, fil)
    unfiltered = search(term)

    paginator = Paginator(policies, 15)

    page = request.GET.get('page')

    try:
        policies = paginator.get_page(page)
    except PageNotAnInteger:
        policies = paginator.get_page(1)
    except EmptyPage:
        policies = paginator.get_page(paginator.num_pages)

    return render(request, 'website/policy_list.html', {'policies': policies, 'all': unfiltered, 'max_pages': paginator.num_pages})

# class FacetedSearchView(BaseFacetedSearchView):
#     form_class = FacetedPolicySearchForm
#     facet_fields = ['school', 'published year']
#     template_name = 'policy_list.html'
#     paginate_by = 3
#     context_object_name = 'object_list'

# Autocomplete function -- takes text as it is being typed into the search bar, runs a simple prefix search over
# just the "title" field, and returns a list of the matches which will then be displayed as suggestions from the
# search bar to the user

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('search')
        search_qs = search_suggest(q)
        results = []
        for r in search_qs:
            results.append(r.title.lower())
        data = json.dumps(results)
    else:
        data = 'fail'
    data = list(set([n.strip() for n in ast.literal_eval(data)]))[:10]
    print("Text: ", q)
    query_length = len(q)
    #print("Suggestions: ", data)

    # check for 'part' and numbers and maybe skip over ones with commas and limit the length of suggestions
    for i in range(len(data)):
        new_list = data[i].split(" ")
        if query_length < 3:
            #Allow suggestions up to length 2
            if len(new_list) > 1:
                data[i] = ""
                continue
        elif query_length >= 3 and query_length <= 10:
            #Allow suggestions up to length 6
            if len(new_list) > 8:
                data[i] = ""
                continue
        else:
            #Allow suggestions up to length 9
            if len(new_list) > 11:
                data[i] = ""
                continue
        for j in range(len(new_list)):
            if new_list[j] == "part":
                data[i] = " ".join(new_list[:j])
                break
            if not new_list[j].isalpha() and new_list[j] != " ":
                data[i] = " ".join(new_list[:j])
                break
    data = list(set(data))
    data = list(filter(None, data))
    data.sort(key=lambda s: len(s))

    return JsonResponse({ 'suggestions': data })

