from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TopicInfo(models.Model):
    topic_id = models.IntegerField(unique=True)
    event_info = models.TextField(null=True)
    date_count = models.TextField(null=True)
    event_edge = models.TextField(null=True)
    event_node = models.TextField(null=True)
    enetiy_name = models.TextField(null=True)
    entity_event = models.TextField(null=True)
    date_info = models.TextField(null=True)
    heatmap_data = models.TextField(null=True)
    feature_frequent = models.TextField(null=True)
    feature_positive = models.TextField(null=True)
    feature_negative = models.TextField(null=True)
    sentiment_stream = models.TextField(null=True)
    sentiment_piechart = models.TextField(null=True)
    news_top = models.TextField(null=True)
    comment_best = models.TextField(null=True)
    comment_top = models.TextField(null=True)
    comment_famous = models.TextField(null=True)
    comment_question = models.TextField(null=True)
    area_data = models.TextField(null=True)
    entity_profile = models.TextField(null=True)


    def __unicode__(self):
        return self.topic_id