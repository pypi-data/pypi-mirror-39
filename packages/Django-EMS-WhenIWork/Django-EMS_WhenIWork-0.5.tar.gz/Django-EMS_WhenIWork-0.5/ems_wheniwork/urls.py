from django.conf.urls import include, url
from django.views.defaults import page_not_found

from .views import serviceorders
from .views.api.booking import Booking
from .views.api.building import Building
from .views.api.schedule import Schedule
from .views.api.serviceorder import ServiceOrder
from .views.api.shift import Shift
from .views.api.status import Status

urlpatterns = [
    url(r'^$', serviceorders.index, name='ems_wheniwork'),

    # Basic EMS data
    url(r'^api/v1/booking/$', Booking().run),
    url(r'^api/v1/building/$', Building().run),
    url(r'^api/v1/serviceorder/$', ServiceOrder().run),
    url(r'^api/v1/status/$', Status().run),

    url(r'^api/v1/shift/(?P<shift_id>\d+)?$', Shift().run),
    url(r'^api/v1/schedule/$', Schedule().run),
]
