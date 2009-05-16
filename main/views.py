from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from crime.models import Crime


def index(request, template_name='main/index.html'):
    """
    Index page.
    """
    if request.method == 'GET':
        crimes = Crime.objects.all().order_by('-date')[:100]
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crimes': crimes,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)

def most_updated(request, template_name='main/most_updated.html'):
    """
    Return crime reports sort by most updated.
    """
    if request.method == 'GET':
        crimes = Crime.objects.all().order_by('-updated_at')[:100]
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crimes': crimes,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)
