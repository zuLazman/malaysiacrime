from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import CrimeCreateForm, CrimeUpdateForm
from models import Crime


def show(request, id, template_name='crime/show.html'):
    """
    Show a reported crime.
    """
    if request.method == 'GET':
        crime = get_object_or_404(Crime, pk=id)
        return redirect(crime, permanent=True)
    else:
        return HttpResponseRedirect(request.path)

def title(request, slug, template_name='crime/show.html'):
    """
    Show a reported crime by it's slug.
    """
    if request.method == 'GET':
        crime = get_object_or_404(Crime, slug=slug)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crime': crime,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)

def create(request, form_class=CrimeCreateForm, template_name='crime/create.html'):
    """
    Report a crime.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            crime = form.save()
            return redirect(crime)
    elif request.method == 'GET':
        form = form_class()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response(template_name, context)

def update(request, id, form_class=CrimeUpdateForm, template_name='crime/update.html'):
    """
    Update an existing crime report.
    """
    crime = get_object_or_404(Crime, pk=id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=crime)
        if form.is_valid():
            crime = form.save()
            return redirect(crime)
    elif request.method == 'GET':
        crime.password = ""
        form = form_class(instance=crime)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crime': crime,
        'form': form,
    })
    return render_to_response(template_name, context)

