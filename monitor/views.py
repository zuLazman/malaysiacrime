from datetime import datetime
from uuid import uuid1

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import Context, RequestContext, Template
from django.template.loader import get_template

from models import Moniton
from forms import SubscribeForm


def subscribe(request, form_class=SubscribeForm, template_name='monitor/subscribe.html'):
    """
    Subscribe to monitor an area.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            moniton = form.save(commit=False)
            moniton.add_uuid = uuid1().hex # uuid used for subscribe confirmation.
            moniton.del_uuid = uuid1().hex # uuid used foru nsubscribeconfirmation.
            moniton.add_date = datetime.now() # Register but unconfirm timestamp.
            moniton.save()

            # Send confirmation email. Let exception bubble up to trigger email to ADMIN.
            send_mail(
                'Confirmation of Malaysia Crime Monitor subscription',
                get_template('monitor/subscribe_email.txt').render(Context({'add_uuid': moniton.add_uuid})),
                'dontreply@malaysiacrime.com', [moniton.email])

            return redirect('monitor-subscribe-done', uuid=moniton.add_uuid)
    elif request.method == 'GET':
        form = form_class()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response(template_name, context)

def subscribe_done(request, uuid, template_name='monitor/subscribe_done.html'):
    """
    Show successfully sent request for confirmation email.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, add_uuid=uuid)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'moniton': moniton,
    })
    return render_to_response(template_name, context)

def subscribe_confirm(request, uuid, template_name='monitor/subscribe_confirm.html'):
    """
    Registered the moniton. And show successfully registered.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, add_uuid=uuid)
        moniton.registered = True
        moniton.add_uuid = uuid1().hex # Reset uuid for starting unscubscribe process.
        moniton.add_date = datetime.now() # The confirmation timestamp.
        moniton.save()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'moniton': moniton,
    })
    return render_to_response(template_name, context)

def unsubscribe_done(request, uuid, template_name='monitor/unsubscribe_done.html'):
    """
    Send email to confirm unsubscribe.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, add_uuid=uuid)

        # Send confirmation email. Let exception bubble up to trigger email to ADMIN.
        send_mail(
            'Confirmation of Malaysia Crime Monitor unsubscription',
            get_template('monitor/unsubscribe_email.txt').render(Context({'del_uuid': moniton.del_uuid})),
            'dontreply@malaysiacrime.com', [moniton.email])
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'moniton': moniton,
    })
    return render_to_response(template_name, context)

def unsubscribe_confirm(request, uuid, template_name='monitor/unsubscribe_confirm.html'):
    """
    Unregistered the moniton. And show successfully unregistered.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, del_uuid=uuid)
        moniton.delete()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'moniton': moniton,
    })
    return render_to_response(template_name, context)

def area(request, uuid, template_name='monitor/area.html'):
    """
    Show the monitoring area.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, add_uuid=uuid)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'moniton': moniton,
    })
    return render_to_response(template_name, context)
