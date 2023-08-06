import logging

from django.forms.models import model_to_dict
from ems_client.service import Service

from . import RESTDispatch

logger = logging.getLogger(__name__)


class Booking(RESTDispatch):
    def __init__(self):
        self._service_api = Service()
        self._audit_log = logging.getLogger('audit')

    def GET(self, request, **kwargs):
        params = {
            "start_date": request.GET.get('StartDate'),
            "end_date": request.GET.get('EndDate'),
            "statuses": request.GET.get('Statuses'),
        }
        if params['statuses']:
            params['statuses'] = params['statuses'].split(',')

        bookings = self._service_api.get_bookings(**params)

        bookings2 = []
        for booking in bookings:
            booking2 = model_to_dict(booking)
            for key in booking2.keys():
                if hasattr(booking, 'get_%s_display' % key):
                    booking2['dv_%s' % key] = getattr(
                        booking, 'get_%s_display' % key)()
            bookings2.append(booking2)

        return self.json_response(bookings2)
