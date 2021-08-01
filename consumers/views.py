
from django.http.response import HttpResponse
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from consumers.util import validate_webhook_request

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
    return HttpResponse('OK')


@csrf_exempt
def echo(request):
    # print("key", request.POST.get('key'))
    print('value', request.POST.get('value'))
    return HttpResponse(request.POST.get('value'))