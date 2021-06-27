from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=32, default="new job")
    code = models.TextField()
    times_to_run = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} {self.id}"

    def run(self):
        from jobmanager.tasks import run_job

        for n in range(0, self.times_to_run):
            run_job.delay(self.id)
        return True

    def run_main(self):
        state = JobRun(job=self)
        state.save()

        try:
            state.state = "running"
            state.save()

            exec(self.code)

            state.status = "ok"
            state.save()
        except Exception:
            state.status = "error"
            state.save()
        finally:
            state.state = "done"
            state.save()
            pass


class JobRun(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    state = models.CharField(
        max_length=16,
        default="not-run",
        choices=(("not-run", "not-run"), ("running", "running"), ("done", "done")),
    )

    status = models.CharField(
        max_length=16,
        default="none",
        choices=(("none", "none"), ("ok", "ok"), ("error", "error")),
    )

    def __str__(self):
        return f"{self.job.id} {self.state} {self.status}"
