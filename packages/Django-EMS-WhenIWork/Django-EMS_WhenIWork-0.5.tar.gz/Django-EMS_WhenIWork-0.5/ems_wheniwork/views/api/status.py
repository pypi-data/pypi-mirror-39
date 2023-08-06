import logging

from django.forms.models import model_to_dict
from ems_client.service import Service

from . import RESTDispatch

logger = logging.getLogger(__name__)


class Status(RESTDispatch):
    def __init__(self):
        self._service_api = Service()
        self._audit_log = logging.getLogger('audit')

    def GET(self, request, **kwargs):
        statuses = self._service_api.get_statuses()

        statuses2 = []
        for status in statuses:
            status2 = model_to_dict(status)
            for key in status2.keys():
                if hasattr(status, 'get_%s_display' % key):
                    status2['dv_%s' % key] = getattr(
                        status, 'get_%s_display' % key)()
            statuses2.append(status2)

        return self.json_response(statuses2)
