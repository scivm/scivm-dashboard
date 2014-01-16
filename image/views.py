from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _
from image.models import Image
from image.forms import ImageForm
from scivm import tasks

@login_required
def index(request):
    thisuser = User.objects.get(username=request.user.username)
    images = Image.objects.filter(owner__pk=thisuser.pk)
    ctx = {
        'images': images
    }
    return render_to_response('image/index.html', ctx,
        context_instance=RequestContext(request))

@login_required
def add_image(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST)
        form.owner = request.user
        if form.is_valid():
            ptype = form.save(commit=False)
            ptype.owner = request.user
            ptype.save()
            return redirect(reverse('image.views.index'))
    ctx = {
        'form': form
    }
    return render_to_response('image/add_image.html', ctx,
        context_instance=RequestContext(request))

@login_required
def remove_image(request, image_id):
    h = Image.objects.get(id=image_id)
    h.delete()
    messages.add_message(request, messages.INFO, _('Removed') + ' {0}'.format(
        h.name))
    return redirect('image.views.index')

@login_required
def import_image(request):
    repo = request.POST.get('repo_name')
    if repo:
        tasks.import_image.delay(repo)
        messages.add_message(request, messages.INFO, _('Importing') + \
            ' {}'.format(repo) + _('.  This could take a few minutes.'))
    return redirect('image.views.index')

@login_required
def build_image(request):
    path = request.POST.get('path')
    tag = request.POST.get('tag', None)
    if path:
        tasks.build_image.delay(path, tag)
        messages.add_message(request, messages.INFO, _('Building.  This ' \
            'could take a few minutes.'))
    return redirect('image.views.index')
