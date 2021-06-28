from django.shortcuts import render
from django.views.generic import ListView
from .models import Job, JobRun


def root(request):
    return render(request, "jobmanager/index.html", {})


class JobView(ListView):
    model = Job


class JobRunView(ListView):
    model = JobRun
