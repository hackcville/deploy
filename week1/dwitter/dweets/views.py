from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from jsonschema import validate
from django.utils import timezone

from .models import Dweet, User


def index(request):
    dweets = Dweet.objects.order_by('date')
    return render(request, 'index.html', {'dweets': dweets})


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
