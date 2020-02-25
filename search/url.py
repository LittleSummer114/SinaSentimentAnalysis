from django.conf.urls import url

from search import views as search_views

app_name = 'search'
urlpatterns = [
    url(r'^introduction', search_views.introduction, name='introduction'),
    url(r'^getTopicList', search_views.getTopicList, name='getTopicList'),

    url(r'^$', search_views.search_index, name='index'),
]
