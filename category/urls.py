from django.conf.urls import url

from category import views as category_views

app_name = 'category'
urlpatterns = [

    url(r'^getTopicList', category_views.getTopicList, name='getTopicList'),

    url(r'^', category_views.categoryIndex, name = 'category_page'),

]