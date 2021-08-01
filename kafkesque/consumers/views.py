from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def echo(request):
    # print("key", request.POST.get('key'))
    print("value", request.POST.get("value"))
    return HttpResponse(request.POST.get("value"))
