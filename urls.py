"""Generic base url directives.

These directives will redirect requests to app specific pages
It will also provide redundancy in possible names."""

from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#(r'^', 'django.views.generic.simple.direct_to_template', {'template': 'maintenance.html'}),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^accounts/login/', 'django.contrib.auth.views.login'),

	(r'^mouse/', include('mousedb.animal.urls.mouse')),
	(r'^mice/', include('mousedb.animal.urls.mouse')),
	(r'^animals?/', include('mousedb.animal.urls.mouse')),
	(r'^strains?/', include('mousedb.animal.urls.strain')),
	(r'^dates?/', include('mousedb.animal.urls.date')),
	(r'^breedings?/', include('mousedb.animal.urls.breeding')),
	(r'^breeding_cages?/', include('mousedb.animal.urls.breeding')),
	url(r'^todo/', include('mousedb.animal.urls.todo'), name="todo-list"),

	(r'^experiments?/', include('mousedb.data.urls.experiment')),
	(r'^study/', include('mousedb.data.urls.study')),
	(r'^studies/', include('mousedb.data.urls.study')),
	url(r'^treatments?/', include('mousedb.data.urls.treatment')),
	(r'^parameters?/', include('mousedb.data.urls.parameter')),

	(r'^plugs?/', include('mousedb.timed_mating.urls')),
	(r'^plugevents?/', include('mousedb.timed_mating.urls')),
	(r'^plug_events?/', include('mousedb.timed_mating.urls')),
	(r'^timedmatings?/', include('mousedb.timed_mating.urls')),
	(r'^timed_matings?/', include('mousedb.timed_mating.urls')),
	
	url(r'^specs?/$', 'django.views.generic.simple.direct_to_template', {'template': 'specs.html'}, name="specs"),
	url(r'^index/$', 'mousedb.views.home', name="home"),
)

