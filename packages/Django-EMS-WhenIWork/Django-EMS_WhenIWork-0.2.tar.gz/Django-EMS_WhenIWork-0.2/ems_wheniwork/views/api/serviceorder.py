import logging

from django.forms.models import model_to_dict
from ems_client.service import Service

from . import RESTDispatch

logger = logging.getLogger(__name__)


class ServiceOrder(RESTDispatch):
    def __init__(self):
        self._service_api = Service()
        self._audit_log = logging.getLogger('audit')

    def GET(self, request, **kwargs):
        serviceorders = self._service_api.get_service_order_details(
            start_date=request.GET.get('StartDate'),
            end_date=request.GET.get('EndDate'))

        serviceorders2 = []
        for serviceorder in serviceorders:
            serviceorders2.append(model_to_dict(serviceorder))

        return self.json_response(serviceorders2)
