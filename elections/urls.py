from django.conf.urls import url, include
from . import views
from django.conf.urls import handler404

handler404 = 'elections.views.custom_404'

app_name = 'elections'
urlpatterns = [
    url(r'^$', views.index, name = 'home'),
    url(r'^areas/(?P<area>[가-힣]+)/$', views.areas),
    url(r'^areas/(?P<area>[가-힣]+)/results$', views.results),
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls),
	url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates),

]
