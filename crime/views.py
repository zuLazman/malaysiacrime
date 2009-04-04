from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from forms import CrimeCreateForm, CrimeUpdateForm
from models import Crime


def show(request, id, template_name='crime/show.html'):
    """
    Show a reported crime.
    """
    if request.method == 'GET':
        crime = get_object_or_404(Crime, pk=id)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crime': crime,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)

def create(request, template_name='crime/create.html'):
    """
    Report a crime.
    """
    if request.method == 'POST':
        form = CrimeCreateForm(request.POST)
        if form.is_valid():
            crime = form.save()
            return HttpResponseRedirect(reverse('crime-show', args=[crime.id]))
    elif request.method == 'GET':
        form = CrimeCreateForm()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response(template_name, context)
    
def update(request, id, template_name='crime/update.html'):
    """
    Update an existing crime report.
    """
    crime = get_object_or_404(Crime, pk=id)
    
    if request.method == 'POST':
        form = CrimeUpdateForm(request.POST, instance=crime)
        if form.is_valid():
            crime = form.save()
            return HttpResponseRedirect(reverse('crime-show', args=[crime.id]))
    elif request.method == 'GET':
        crime.password = ""
        form = CrimeUpdateForm(instance=crime)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crime': crime,
        'form': form,        
    })
    return render_to_response(template_name, context)

