from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _
from volume.models import Volume
from volume.forms import VolumeForm

@login_required
def index(request):
    thisuser = User.objects.get(username=request.user.username)
    volumes = Volume.objects.filter(owner__pk=thisuser.pk)
    ctx = {
        'volumes': volumes
    }
    return render_to_response('volume/index.html', ctx,
        context_instance=RequestContext(request))

@login_required
def add_volume(request):
    form = VolumeForm()
    if request.method == 'POST':
        form = VolumeForm(request.POST)
        form.owner = request.user
        if form.is_valid():
            ptype = form.save(commit=False)
            ptype.owner = request.user
            ptype.save()
            return redirect(reverse('volume.views.index'))
    ctx = {
        'form': form
    }
    return render_to_response('volume/add_volume.html', ctx,
        context_instance=RequestContext(request))

@login_required
def remove_volume(request, volume_id):
    h = Volume.objects.get(id=volume_id)
    h.delete()
    messages.add_message(request, messages.INFO, _('Removed') + ' {0}'.format(
        h.name))
    return redirect('volume.views.index')

@login_required
def snapshot_volume(request, volume_id):
    h = Volume.objects.get(id=volume_id)
    messages.add_message(request, messages.INFO, _('Snapshot Taken') + ' {0}'.format(
        h.name))
    return redirect('volume.views.index')


