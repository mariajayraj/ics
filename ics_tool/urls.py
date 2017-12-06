from django.conf.urls import url, patterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.core.urlresolvers import reverse

from . import views, user_views, donations

app_name='ics_tool'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^add_donor', views.add_donor, name='add_donor'),
    url(r'^search_donor', views.search_donor, name='search_donor'),
    url(r'^edit_donor', views.edit_donor, name='edit_donor'),
    url(r'^feedback', views.feedback, name='feedback'),
    url(r'^add_donations', donations.add_donations, name='add_donations'),
    url(r'^login/$', user_views.user_login, name='login'),
    url(r'^logout', user_views.user_logout, name='logout'),
    url(r'^add_inkind', views.add_inkind, name='add_inkind'),
    url(r'^add_items', views.add_items, name='add_items'),
    url(r'^add_events', views.add_events, name='add_events'),
    url(r'^donor_report', views.donor_report, name='donor_report'),

]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
