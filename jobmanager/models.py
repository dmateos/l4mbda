from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=32, default="new job")
    code = models.TextField()
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
    run_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.id} {self.state} {self.status} {self.run_count}"

    def run(self):
        from jobmanager.tasks import run_job

        run_job.delay(self.id)
        return True

    def run_main(self):
        self.state = "running"
        self.save()

        try:
            exec(self.code)
            self.status = "ok"
        except Exception:
            self.status = "error"
        finally:
            self.state = "done"
            self.run_count += 1
            self.save()

    def job_status(self):
        pass


class JobRun(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job.id}"
