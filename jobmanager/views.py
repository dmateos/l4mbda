from django.http import HttpResponse
from django.shortcuts import render


def root(request):
    return render(request, "jobmanager/index.html", {})


def test(request):
    return HttpResponse("hello world")
