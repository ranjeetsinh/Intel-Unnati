from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/contracts/(?P<contract_id>\w+)/$', consumers.ContractConsumer.as_asgi()),
]
