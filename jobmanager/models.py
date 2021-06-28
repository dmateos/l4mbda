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
            state.set_state("running")
            exec(self.code)
            state.set_status("ok")
        except Exception as e:
            state.set_status("error")
            state.set_job_message(str(e))
        finally:
            state.set_state("done")
            pass


class JobRun(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_message = models.TextField(default="")

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

    def set_state(self, state):
        self.state = state
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    def set_job_message(self, message):
        self.job_message = message
        self.save()


class JobInput(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def _str__(self):
        return f"{self.job.id}"
