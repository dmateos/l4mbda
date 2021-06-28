from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .models import Job, JobRun


def root(request):
    return render(request, "jobmanager/index.html", {})


def run_job(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.run()
    return HttpResponseRedirect("/jobs")


class JobView(ListView):
    model = Job


class JobRunView(ListView):
    model = JobRun
