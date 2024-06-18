import threading
import time
import datetime
from src.services.task_service import TaskService
from src.repositories.redis_repository import RedisRepository


def worker():
    while True:
        task = RedisRepository.pop_task_from_queue()
        if task:
            task_id = task["task_id"]
            date = task["date"]
            supid = task["supid"]
            TaskService.update_task_status(task_id, date, supid, "in-progress",
                                           start_time=datetime.datetime.now().isoformat())

            process_task(date, supid)

            TaskService.update_task_status(task_id, date, supid, "completed",
                                           end_time=datetime.datetime.now().isoformat())
        time.sleep(5)


def process_task(date: str, supid: int):
    # Placeholder for actual task processing logic
    time.sleep(5)


worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()
