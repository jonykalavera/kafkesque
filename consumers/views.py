import logging
from django.http.response import HttpResponse
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .util import validate_webhook_request
from .models import WebhookConfig


logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()



@require_POST
async def register_webhook(request):
    params = request.POST
    validate_webhook_request(params)

    await channel_layer.send(
        'kafka-consume',
        {
            'type': 'kafka.consume',
            'topics': [params['topic']],
            'name': 'someoneelse', # TODO: Figure out name.
            'format': params.get('format', 'json'),
            'auto.offset.reset': params.get('offset', 'earliest'),
            'webhook': params['webhook']
        },
    )

    # Check if exactly the same config already exists
    _, created = WebhookConfig.objects.update_or_create(
        url=params['webhook'],
        topic=params['topic'],
        defaults={
            'serialization_format': params['format'],
            'ts_expire': params.get('ts_expire'),
            'batch_size': params.get('batch_size'),
            'batch_max_interval': params.get('max_batch_interval')
        }
    )
    if created:
        logger.info('Created new webhook for URL: %s, topic: %s', params['webhook'], params['topic'])
    else:
        logger.info('Updated webhook for URL: %s, topic: %s', params['webhook'], params['topic'])

    return HttpResponse('OK')


@csrf_exempt
def echo(request):
    # print("key", request.POST.get('key'))
    print('value', request.POST.get('value'))
    return HttpResponse(request.POST.get('value'))