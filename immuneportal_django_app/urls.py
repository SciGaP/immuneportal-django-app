from django.conf.urls import url, include
from django.conf.urls.static import static

from . import views

app_name = 'immuneportal_django_app'
urlpatterns = [
    url(r'^expviz/', views.expviz, name="expviz"),
    #url(r'^image_view/', views.image_view, name="image_view"),
    #url(r'^both/', views.both, name="both"),
    #url(r'^upset_view/', views.upset_view, name="upset_view"),
    #url(r'^hlaload_view/', views.hlaload_view, name="hlaload_view"),
    #git url(r'^delete/', views.delete, name="delete"),
    #url(r'^splicetable/', views.splice_res, name="splice"),
    #url(r'^languages/', views.languages, name="languages"),
] 
