from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.db.models import get_model


crime_model = get_model('crime', 'crime')


def index(request, template_name='main/index.html'):
    """
    Index page.
    """
    if request.method == 'GET':
        crimes = crime_model.objects.all().order_by('-date')[:100]
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crimes': crimes,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)

def recent_updated(request, template_name='main/recent_updated.html'):
    """
    Return crime reports sort by recent updated.
    """
    if request.method == 'GET':
        crimes = crime_model.objects.all().order_by('-updated_at')[:100]
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crimes': crimes,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)

    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'crimes': crimes,
        'now': datetime.now(),
    })
    return render_to_response(template_name, context)
