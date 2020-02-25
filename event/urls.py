from django.conf.urls import url

from event import views as event_views

# app_name = 'event'
urlpatterns = [
    url(r'^', event_views.eventIndex, name = 'eventPage'),

    # url(r'^(?P<tid>=[0-9]+)$', topic_views.topic_index, name = 'topic_page'),
]

