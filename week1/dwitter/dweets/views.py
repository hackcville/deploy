from django.shortcuts import render
from .models import Dweet, User


def index(request):
    dweets = Dweet.objects.order_by('date')
    return render(request, 'index.html', {'dweets': dweets})
