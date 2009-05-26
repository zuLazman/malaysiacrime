import logging, smtplib
from datetime import datetime

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import get_model
from django.template import Context
from django.template.loader import get_template

from monitor.models import Log, Moniton

crime_model = get_model('crime', 'crime')


class Command(BaseCommand):
    """
    Called by cron job to iterate thru all monitons and send emails accordingly.
    """
    def handle(self, *args, **options):
        now = datetime.fromtimestamp(int(args[0]))
        try:
            last = Log.objects.latest('start')
        except:
            # No record yet, so create the very first one. Try again tomorrow.
            Log.objects.create(start=now, end=now)
            return

        # Create log instance and record start time.
        log = Log.objects.create(start=now)

        # Iterate all monitons.
        for m in Moniton.objects.filter(registered=True).all():
            crimes = crime_model._default_manager.filter(
                created_at__gt=last.start,
                lat__lte=m.north,
                lat__gte=m.south,
                lng__lte=m.east,
                lng__gte=m.west)
            try:
                send_mail('[Malaysia Crime] Notification of Crimes',
                    get_template('monitor/notification_email.txt').render(Context({'moniton': m, 'crimes': crimes})),
                    'noreply@malaysiacrime.com', [m.email])
            except smtplib.SMTPException, e:
                logging.error(e)
                mail_admins('Monitor Error', e)

        # Record end time and calculate duraction.
        log.end = datetime.now()
        log.save()
