import os

from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from consumers import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "channel": ChannelNameRouter({
        "kafka-consume": consumers.KafkaConsumerConsumer.as_asgi(),
        # "thumbnails-delete": consumers.PrintConsumer.as_asgi(),
    }),
})