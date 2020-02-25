from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CommentInfo(models.Model):
    comment_id = models.IntegerField(unique=True)
    comment_newsId = models.CharField(max_length = 25, null = True)
    comment_time = models.CharField(max_length = 25, null = True)
    comment_verify = models.IntegerField(default = 0)
    comment_nick = models.CharField(max_length = 100, null = True)
    comment_area = models.CharField(max_length = 50, null = True)
    comment_against = models.IntegerField(default = 0)
    comment_body = models.TextField(null = True)
    preprocess = models.TextField(null = True)
    postagging = models.TextField(null = True)
    syntactic = models.TextField(null = True)
    pv_word = models.TextField(null = True)
    pv_modifierword = models.TextField(null = True)
    keywords = models.TextField(null = True)
    tag = models.IntegerField(default = -1)
    sentiment = models.IntegerField(default = -1)
    mutisentiment = models.TextField(null = True)
    topic_id = models.IntegerField(default = -1)

    comment_news_url = models.CharField(max_length = 100, null = True)
    comment_news_title = models.CharField(max_length = 25, null = True)
    comment_topic_name = models.CharField(max_length = 100, null = True)

    def __unicode__(self):
        return self.comment_id