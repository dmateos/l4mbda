from celery import Celery

app = Celery("tasks", broker="pyamqp://guest@localhost//")


@app.task
def run_job(x):
    print(x)
