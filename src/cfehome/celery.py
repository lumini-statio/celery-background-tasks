import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")

app = Celery("cfehome")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "fetch-pokemon": {
        "task": "movies.tasks.api",
        "schedule": crontab(minute='*'),
    },
}

app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_format='%(asctime)s [%(levelname)s] [%(processName)s] %(message)s',
    worker_task_log_format='%(asctime)s [%(levelname)s] [%(task_name)s] %(message)s',
)