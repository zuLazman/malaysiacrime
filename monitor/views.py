from datetime import datetime
from uuid import uuid1

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
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
            moniton.add_uuid = uuid1().hex # uuid used for confirmation.
            moniton.add_date = datetime.now() # Register but unconfirm timestamp.
            moniton.save()

            # Send confirmation email. Let exception bubble up to trigger email to ADMIN.
            send_mail(
                'Confirmation of Malaysia Crime Monitor subscription',
                get_template('monitor/subscribe_email.txt').render(Context({'add_uuid': moniton.add_uuid})),
                'dontreply@malaysiacrime.com', [moniton.email])

            return redirect('%s?uuid=%s' % (reverse('monitor-subscribe-done'), moniton.add_uuid))
    elif request.method == 'GET':
        form = form_class()
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response(template_name, context)

def subscribe_done(request, template_name='monitor/subscribe_done.html'):
    """
    Show successfully sent request for confirmation email.
    """
    if request.method == 'GET':
        moniton = get_object_or_404(Moniton, add_uuid=request.GET.get('uuid', 'INVALID'))
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'email': moniton.email,
    })
    return render_to_response(template_name, context)
