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

    def run(self):
        from jobmanager.tasks import run_job

        run_job.delay(self.id)
        return True

    def run_main(self):
        self.state = "running"
        self.save()

        print(self.code)
        exec(self.code)

        self.state = "done"
        self.save()
