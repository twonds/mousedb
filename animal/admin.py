"""Admin site settings for the animal app."""

from mousedb.animal.models import Strain, Animal, Breeding, Cage
from django.contrib import admin
import datetime

class AnimalInline(admin.TabularInline):
    """Provides an inline tabular formset for animal objects.  
	
	Not currently used.
	"""
    model = Animal
    fields = (
       'Strain', 
       'Background', 
       'MouseID',
       'Cage', 
       'Genotype', 
       'Gender', 
       'Born', 
       'Weaned', 
       'Generation', 
       'Markings', 
       'Notes', 
       'Rack', 
       'Rack_Position')
    radio_fields = {
       "Gender": admin.HORIZONTAL,
       "Strain":admin.HORIZONTAL, 
       "Background": admin.HORIZONTAL, 
       "Genotype": admin.HORIZONTAL }

class AnimalAdmin(admin.ModelAdmin):
    """Provides parameters for animal objects within the admin interface."""
    fieldsets = (
        (None, {
            'fields': (
                'Strain',
                'Background',
                'MouseID',
                'Cage', 
                'Genotype', 
                'Gender', 
                'Born', 
                'Weaned', 
                'Backcross', 
                'Generation', 
                'Markings', 
                'Notes', 
                'Breeding', 
                'Rack', 
                'Rack_Position')
        }),
    ('Animal Death Information', {
        'classes' : ('collapse',),
        'fields' : ('Death', 'Cause_of_Death', 'Alive'),
        }),
    )
    raw_id_fields = ("Breeding",)
    list_display = (
        'MouseID', 
        'Rack', 
        'Rack_Position', 
        'Cage', 
        'Markings',
        'Gender', 
        'Genotype',
        'Strain', 
        'Background', 
        'Generation', 
        'Backcross', 
        'Born', 
        'Alive',
        'Death')
    list_filter = (
        'Alive',
        'Strain', 
        'Background',
        'Gender',
        'Genotype',
        'Backcross')
    search_fields = ['MouseID', 'Cage']
    radio_fields = {
        "Gender": admin.HORIZONTAL,
        "Strain":admin.HORIZONTAL,
        "Background": admin.HORIZONTAL,
        "Genotype": admin.HORIZONTAL,
        "Cause_of_Death": admin.HORIZONTAL}
    actions = ['mark_sacrificed']
    def mark_sacrificed(self, request, queryset):
        """An admin action for marking several animals as sacrificed.
		
        This action sets the selected animals as Alive=False, Death=today and Cause_of_Death as sacrificed.  
        To use other paramters, mice muse be individually marked as sacrificed.
        This action also shows as the output the number of mice sacrificed.
        """
        rows_updated = queryset.update(
            Alive=False,
            Death=datetime.date.today(),
            Cause_of_Death='Sacrificed')
        if rows_updated == 1:
            message_bit = "1 animal was"
        else:
            message_bit = "%s animals were" % rows_updated
        self.message_user(
            request,"%s successfully marked as sacrificed." % message_bit)
    mark_sacrificed.short_description = "Mark Animals as Sacrificed"
admin.site.register(Animal, AnimalAdmin)

class StrainAdmin(admin.ModelAdmin):
    """Settings in the admin interface for dealing with Strain objects."""
    fields = (
        'Strain',
        'Strain_slug',
        'Comments')
    prepopulated_fields = {"Strain_slug": ("Strain",)}
admin.site.register(Strain, StrainAdmin)

class BreedingAdmin(admin.ModelAdmin):
    """Settings in the admin interface for dealing with Breeding objects."""
    list_display = (
        'Cage',
        'CageID',
        'Start',
        'Rack',
        'Rack_Position',
        'Strain',
        'Crosstype',
        'BreedingName',
        'Notes',
        'Active')
    list_filter = (
        'Timed_Mating',
        'Strain',
        'Active',
        'Crosstype')
    fields = (
        'Male',
        'Females',
        'Timed_Mating',
        'Cage',
        'CageID', 
        'Rack', 
        'Rack_Position',
        'BreedingName',
        'Strain',
        'Start',
        'End',
        'Active',
        'Crosstype',
        'Notes')
    ordering = ('Active', 'Start')
    search_fields = ['Cage', ]
    raw_id_fields = (
        "Male",
        "Females")
    radio_fields = {
        "Crosstype": admin.VERTICAL,
        "Strain": admin.HORIZONTAL}
admin.site.register(Breeding, BreedingAdmin)

class CageAdmin(admin.ModelAdmin):
    """Settings in the admin interface for dealing with Cage objects.
	
	Not currently implemented as the Cage model is not yet implemented."""
    fields = ('Barcode', 'Rack', 'Rack_Position')
    list_display = ('Barcode', 'Rack', 'Rack_Position')
    list_filter = ('Rack',)
admin.site.register(Cage, CageAdmin)
