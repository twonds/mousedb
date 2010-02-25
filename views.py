"""This module defins base views.

The todo and home pages are defined by this module."""
import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import connection

from mousedb.animal.models import Animal, Strain

@login_required
def todo(request):
    """This view defines the todo list pages.

    This page takes a /todo page and returns several important book-keeping tasks.
    For these purposes, weaned pups are defined by WEAN_AGE variable in localsettings.py
    Default is pups < 30 days old and that have not been weaned."""
    eartag_list = Animal.objects.filter(MouseID__isnull=True, Alive=True).\
order_by('Strain','Background','Rack','Cage')
    genotype_list = Animal.objects.filter(Genotype="N.D.", Alive=True).\
exclude(Strain__Strain="C57BL/6").order_by('Strain','Background','Rack','Cage')
    wean = datetime.date.today() - datetime.timedelta(days=30)
    wean_list = Animal.objects.filter(Born__gt=wean).\
filter(Weaned=None,Alive=True).exclude(Strain=2).\
order_by('Strain','Background','Rack','Cage')
    return render_to_response('todo.html', {
        'eartag_list':eartag_list,
        'wean_list':wean_list, 
        'genotype_list':genotype_list
        },
        context_instance=RequestContext(request))

@login_required
def home(request):
    """This is the default home page.

    This page lists both total and current animals, cages and strains. 
    """
    cursor = connection.cursor()
    cage_list = cursor.execute("select distinct Cage from animal_animal")
    cage_list_current = cursor.execute\
("select distinct Cage from animal_animal where Alive='1'")
    animal_list = Animal.objects.all()
    animal_list_current = Animal.objects.filter(Alive=True)
    strain_list = Strain.objects.all()
    strain_list_current = Strain.objects.filter(animal__Alive=True)
    return render_to_response('home.html', {
        'animal_list':animal_list,
        'animal_list_current':animal_list_current,
        'strain_list':strain_list, 
        'strain_list_current':strain_list_current, 
        'cage_list':cage_list, 
        'cage_list_current':cage_list_current
        },
        context_instance=RequestContext(request))

