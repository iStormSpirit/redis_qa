import datetime
import multiprocessing
import random
import threading
import time

from loguru import logger

from src.repositories.redis_repository import RedisRepository
from src.services.task_service import TaskService


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

            RedisRepository.unlock_task(task_id, date, supid)
        # time.sleep(1)
        # if RedisRepository.lock_task(task_id, date, supid):
        #     TaskService.update_task_status(task_id, date, supid, "in-progress",
        #                                    start_time=datetime.datetime.now().isoformat())
        #
        #     process_task(date, supid)
        #
        #     TaskService.update_task_status(task_id, date, supid, "completed",
        #                                    end_time=datetime.datetime.now().isoformat())
        #
        #     RedisRepository.unlock_task(task_id, date, supid)


def process_task(date: str, supid: int):
    # Placeholder for actual task processing logic
    logger.info(f"start proces task {date}, supid {supid}")
    time.sleep(1)


worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()

# def start_workers():
#     num_workers = max(1, multiprocessing.cpu_count())
#     logger.info(f"num_workers {num_workers}")
#
#     processes = []
#     for _ in range(1, num_workers + 1):
#         p = multiprocessing.Process(target=worker)
#         p.start()
#         processes.append(p)
#     for p in processes:
#         p.join()
#
#     logger.info(f"num_workers {processes}")
#
#
# if __name__ == "__main__":
#     start_workers()
