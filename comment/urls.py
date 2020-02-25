from django.conf.urls import url

from comment import views as comment_views

app_name = 'comment'
urlpatterns = [
    url(r'^getPieChartData', comment_views.getPieChartData, name = 'getPieChartData'),
    url(r'^getParserTreeData', comment_views.getParserTreeData, name = 'getParserTreeData'),
    url(r'^', comment_views.commentIndex, name = 'commentPage'),



    # url(r'^(?P<tid>=[0-9]+)$', topic_views.topic_index, name = 'topic_page'),
]

