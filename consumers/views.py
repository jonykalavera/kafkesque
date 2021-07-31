from django.http.response import HttpResponse
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt

channel_layer = get_channel_layer()

async def hello(request):
    await channel_layer.send(
        "kafka-consume",
        {
            "type": "kafka.consume",
            "topics": ["quickstart-events"],
            "name": "someoneelse",
            "format": "json",
            "auto.offset.reset": "earliest",
            "webhook": "http://localhost:8000/echo/"
        },
    )
    return HttpResponse('OK')

@csrf_exempt
def echo(request):
    # print("key", request.POST.get('key'))
    print('value', request.POST.get('value'))
    return HttpResponse(request.POST.get('value'))