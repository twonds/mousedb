"""These modules define extra context processors.

These contexts are provided to every view in which a context is passed."""

from mousedb.groups.models import Group

def group_info(request):
    """This context processor provides group information to all templates."""
    group = Group.objects.get(pk=1)
    return {'group': group}
