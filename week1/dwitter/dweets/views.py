from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from jsonschema import validate
from django.utils import timezone

from .models import Dweet, User


def index(request):
    dweets = Dweet.objects.order_by('-date')
    paginator = Paginator(dweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})


schema_post = {
    'type': 'object',
    'properties': {
        'user': {
            'type': 'string'
        },
        'message': {
            'type': 'string'
        },
    }
}


@csrf_exempt
def post(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))

        try:
            validate(instance=body, schema=schema_post)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request body!',
                'error': str(e)
            })

        try:
            user = User.objects.get(name=body['user'])
        except:
            user = User(name=body['user'])
            user.save()

        dweet = Dweet(user=user, message=body['message'], date=timezone.now())
        dweet.save()

        return JsonResponse({
            'success': True,
            'message': 'Succesfully posted the dweet!'
        })


def dweets(request):
    if request.method == 'GET':
        try:
            count = int(request.GET.get('count'))
        except:
            count = 5

        data = Dweet.objects.order_by('-date')[:count]

        dweets = []
        for dweet in data:
            dweets.append({
                'user': dweet.user.name,
                'message': dweet.message,
                'date': dweet.date
            })

        return JsonResponse({
            'success': True,
            'data': dweets
        })
