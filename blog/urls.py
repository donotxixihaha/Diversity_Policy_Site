from django.urls import path
from . import views
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Added call to the new (10/28) autocomplete function instead of previous one
urlpatterns = [
    path('', views.search_home, name='index_view'),
    path('policy/', views.policy_search, name='policy-search'),
    path('policy_suggest/', views.autocompleteModel, name='policy-suggest')
]

urlpatterns += staticfiles_urlpatterns()