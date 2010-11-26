"""This package defines views for the timed_mating application.

Currently all views are generic CRUD views except for the view in which a plug event is defined from a breeding cage."""

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from mousedb.animal.models import Breeding, Animal
from mousedb.timed_mating.forms import BreedingPlugForm
from mousedb.timed_mating.models import PlugEvents

@login_required
class PlugListView(ListView):
    """This generic view generates a list of all plug events.
	
    This view returns a plug_list object of all pluy events and renders it using plug_list.html.
    This view is restricted to logged in users."""
    
    queryset = PlugEvents.objects.all()
    template_name = plug_list.html'
    context_object_name = plug_list

@login_required	
class PlugDetailView(DetailView):
    """This generic view provides details about a particular plug event.
	
    This view searches all plugevents for a particular primary key (defined in the url) and returns a plug object to plug_detail.html.
    This view is restricted to logged in users."""

    queryset = PlugEvents.objects.all()
    template_name = plug_detail.html
    context_object_name = plug
	
@permission_required('timed_mating.add_plugevents')
class PlugEventCreate(CreateView):
    """This generic view generates a new plug event form.
	
    It renders plug_form and after saving redirects to /mousedb/plug_events.
    This view is restricted to those with the add_plugevents permission."""
	
    model = PlugEvents
    template_name = plug_form.html'
    login_required = True
    post_save_redirect = "/mousedb/plug_events/"
	


@permission_required('timed_mating.add_plugevents')
def breeding_plugevent(request, breeding_id):
    """This view defines a form for adding new plug events from a breeding cage.

    This form requires a breeding_id from a breeding set and restricts the PlugFemale and PlugMale to animals that are defined in that breeding cage."""
    breeding = Breeding.objects.select_related().get(id=breeding_id)
    if request.method == "POST":
        form = BreedingPlugForm(request.POST, request.FILES)
        if form.is_valid():
            plug = form.save(commit=False)
            plug.Breeding_id = breeding.id
            plug.save()
            form.save()
            return HttpResponseRedirect("/mousedb/plug/")
    else:
        form = BreedingPlugForm()
        form.fields["PlugFemale"].queryset = breeding.Females.all()
        form.fields["PlugMale"].queryset = breeding.Male.all()
    return render_to_response('breedingplug_form.html', {'form':form, 'breeding':breeding},context_instance=RequestContext(request))

