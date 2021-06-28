import django.test
from unittest.mock import patch
from .models import Job, JobRun


class TestJobModel(django.test.TestCase):
    @patch("builtins.exec")
    def test_job_run_main_runs_ok(self, mock_exec):
        job = Job.objects.create(code="hello world")
        job.run_main()

        mock_exec.assert_called_with("hello world")
        assert mock_exec.call_count == 1
        for runs in job.jobrun_set.all():
            assert runs.state == "done"
            assert runs.status == "ok"
        assert job.jobrun_set.count() == 1

    @patch("builtins.exec")
    def test_job_run_main_errors(self, mock_exec):
        job = Job.objects.create(code="hello world")
        mock_exec.side_effect = Exception("")

        job.run_main()

        mock_exec.assert_called_with("hello world")
        for runs in job.jobrun_set.all():
            assert runs.state == "done"
            assert runs.status == "error"

    @patch("builtins.exec")
    def test_job_run_main_runs_multiple(self, mock_exec):
        job = Job.objects.create(code="hello world")
        job.run_main()
        job.run_main()

        mock_exec.assert_called_with("hello world")
        assert mock_exec.call_count == 2
        for runs in job.jobrun_set.all():
            assert runs.state == "done"
            assert runs.status == "ok"
        assert job.jobrun_set.count() == 2

    @patch("jobmanager.tasks.run_job")
    def test_job_run(self, mock_run):
        job = Job.objects.create(code="hello world")
        job.run()

        mock_run.delay.assert_called_with(job.id)
        assert mock_run.delay.call_count == 1
        assert True

    @patch("jobmanager.tasks.run_job")
    def test_job_run_multiple(self, mock_run):
        job = Job.objects.create(code="hello world", times_to_run=10)
        job.run()

        mock_run.delay.assert_called_with(job.id)
        assert mock_run.delay.call_count == 10
        assert True

    def test_job_to_str(self):
        job = Job.objects.create(code="hello world", times_to_run=10)
        assert str(job) == f"{job.name} {job.id}"


class TestJobRunModel(django.test.TestCase):
    def test_sets_and_saves_state(self):
        job = Job.objects.create()
        run = JobRun.objects.create(job=job)
        run.set_state("done")
        assert run.state == "done"

    def test_sets_and_save_status(self):
        job = Job.objects.create()
        run = JobRun.objects.create(job=job)
        run.set_status("ok")
        assert run.status == "ok"

    def test_sets_and_saves_job_message(self):
        job = Job.objects.create()
        run = JobRun.objects.create(job=job)
        run.set_job_message("hello world")
        assert run.job_message == "hello world"

    def test_jobrun_to_str(self):
        job = Job.objects.create()
        run = JobRun.objects.create(job=job)
        assert str(run) == f"{job.id} {run.state} {run.status}"
