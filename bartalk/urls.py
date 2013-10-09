from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^api/drinkers/register', 'drinker.views.register', name='register'), )
