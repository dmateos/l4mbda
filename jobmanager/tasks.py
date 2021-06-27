from celery import Celery

app = Celery("tasks", backend="rpc://", broker="pyamqp")


@app.task
def run_job(x, job_state):
    job_state.state = "running"
    job_state.save

    print(x)
    eval(x)

    job_state = "done"
    job_state.save()
