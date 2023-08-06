import logging

from django.forms.models import model_to_dict
from ems_client.service import Service

from . import RESTDispatch

logger = logging.getLogger(__name__)


class Building(RESTDispatch):
    def __init__(self):
        self._service_api = Service()
        self._audit_log = logging.getLogger('audit')

    def GET(self, request, **kwargs):
        buildings = self._service_api.get_buildings()

        buildings2 = []
        for building in buildings:
            buildings2.append(model_to_dict(building))

        return self.json_response(buildings2)
