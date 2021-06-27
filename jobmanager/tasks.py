from celery import Celery
from l4mbda import settings


def build_app():
    redis = "redis://{0}@{1}".format(
        settings.REDIS["default"]["PASSWORD"], settings.REDIS["default"]["HOST"]
    )
    return Celery("tasks", backend=redis, broker=redis)


app = build_app()


@app.task
def run_job(job_state):
    job_state.run_main()
