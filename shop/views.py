from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the main index.")


def register(request):
    return render(request, 'register.html', {"ss":"SSSSSSSS"})
