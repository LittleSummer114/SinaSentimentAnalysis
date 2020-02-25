from django.conf.urls import url

from topic import views as topic_views

app_name = 'topic'
urlpatterns = [

    url(r'^getEventListData', topic_views.getEventListData, name = 'getEventListData'),
    url(r'^getEventEvolutionData', topic_views.getEventEvolutionData, name = 'getEventEvolutionData'),

    url(r'^getFrequentFeatures', topic_views.getFrequentFeatures, name = 'getFrequentFeatures'),
    url(r'^getPositiveFeatures', topic_views.getPositiveFeatures, name = 'getPositiveFeatures'),
    url(r'^getNegativeFeatures', topic_views.getNegativeFeatures, name = 'getNegativeFeatures'),



    url(r'^getTopNewsSet', topic_views.getTopNewsSet, name = 'getTopNewsSet'),
    url(r'^getRecentNewsSet', topic_views.getRecentNewsSet, name = 'getRecentNewsSet'),
    url(r'^getBestNewsSet', topic_views.getBestNewsSet, name = 'getBestNewsSet'),

    url(r'^getBestCommentSet', topic_views.getBestCommentSet, name = 'getBestCommentSet'),
    url(r'^getTopCommentSet', topic_views.getTopCommentSet, name = 'getTopCommentSet'),
    url(r'^getFamousCommentSet', topic_views.getFamousCommentSet, name = 'getFamousCommentSet'),
    url(r'^getQuestionCommentSet', topic_views.getPositiveFeatures, name = 'getQuestionCommentSet'),


    url(r'^getHeatmapData', topic_views.getHeatmapData, name = 'getHeatmapData'),
    url(r'^getAreaData', topic_views.getAreaData, name = 'getAreaData'),


    url(r'^getPieChartData', topic_views.getPieChartData, name = 'getPieChartData'),
    url(r'^getSentimentData', topic_views.getSentimentData, name = 'getSentimentData'),


    url(r'^(?P<cid>[0-9]+)/$', topic_views.turnToCommentPage, name = 'turnToCommentPage'),


    url(r'^', topic_views.topicIndex, name = 'topicPage'),



    # url(r'^(?P<tid>=[0-9]+)$', topic_views.topic_index, name = 'topic_page'),
]

