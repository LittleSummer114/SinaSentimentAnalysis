"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from search import views as search_views

urlpatterns = [
    url(r'^$', search_views.search_index, name = 'search_page'),
    url(r'^introduction/$', search_views.introduction, name = 'introduction_page'),

    url(r'^category/', include('category.urls', namespace='category')),
    url(r'^topic/', include('topic.urls', namespace='topic')),
    url(r'^event/', include('event.urls', namespace='event')),
    url(r'^comment/', include('comment.urls', namespace='comment')),

    url(r'^admin/', admin.site.urls),
]
