"""This file contains tests for the timed_mating application.

These tests will verify generation of a new PlugEvent object.
"""

import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mousedb.timed_mating.models import PlugEvents
from mousedb.animal.models import Breeding, Strain, Animal
 
MODELS = [PlugEvents,]


class Timed_MatingModelTests(TestCase):
    """Test the models contained in the 'timed_mating' app."""

    fixtures = ['test_group',]
    
    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('blah', 'blah@blah.com', 'blah')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.client.login(username='blah', password='blah')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_create_plugevent_minimal(self):
        """This is a test for creating a new PlugEvent object, with only the minimum being entered."""
        new_plugevent = PlugEvents(PlugDate = datetime.date.today() )
        new_plugevent.save()
	test_plugevent = PlugEvents.objects.get(PlugDate = datetime.date.today() )
        self.assertEquals(new_plugevent, test_plugevent)
        self.assertEquals(test_plugevent.__unicode__(), "Plug Event - 1")

    def test_create_plugevent_most_fields(self):
        """This is a test for creating a new PlugEvent object.
        
        This test uses a Breeding, PlugDate, PlugMale and PlugFemale field."""
        new_plugevent = PlugEvents(
            Breeding = Breeding(Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain")),
            PlugDate = datetime.date.today(),
            PlugMale = Animal(
                Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain"), 
                Background = "Mixed", 
                Genotype="-/-", 
                Gender="M"
                ),
            PlugFemale = Animal(
                Strain = Strain(Strain="Test Strain", Strain_slug="Test_Strain"), 
                Background = "Mixed", 
                Genotype="-/-", 
                Gender="M"
                )
            )
        new_plugevent.save()
	test_plugevent = PlugEvents.objects.get(PlugDate = datetime.date.today() )
        self.assertEquals(test_plugevent, new_plugevent)
        self.assertEquals(test_plugevent.__unicode__(), "Plug Event - %i" % test_plugevent.id)

    def test_set_plugevet_inactive(self):
        """This is a test for the automatic inactivation of a cage when the SacrificeDate is entered."""
        plugevent = PlugEvents(PlugDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.__unicode__(), "Plug Event - 1")
        self.assertEquals(plugevent.Active, True)
        plugevent = PlugEvents(id = 1, PlugDate = datetime.date.today(), SacrificeDate = datetime.date.today() )
        plugevent.save()
        self.assertEquals(plugevent.Active, False)

class Timed_MatingViewTests(TestCase):
    """Test the views contained in the 'timed_mating' app."""

    fixtures = ['test_group',]

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')


    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_plugevent_list(self):
        response = self.client.get('/mousedb/timed_mating/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'testuser')


    def test_plugevent_detail(self):
        response = self.client.get('/mousedb/timed_mating/1')
        self.assertEqual(response.status_code, 200)

    def test_plugevent_create(self):
        response = self.client.get('/mousedb/timed_mating/new')
        self.assertEqual(response.status_code, 200)

    def test_plugevent_change(self):
        response = self.client.get('/mousedb/timed_mating/1/edit')
        self.assertEqual(response.status_code, 200)

    def test_plugevent_delete(self):
        response = self.client.get('/mousedb/timed_mating/1/delete')
        self.assertEqual(response.status_code, 200)

    def test_plugevent_delete(self):
        response = self.client.get('/mousedb/timed_mating/breeding/1/new/')
        self.assertEqual(response.status_code, 200)