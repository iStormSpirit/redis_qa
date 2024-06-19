import json
from src.core.config import redis_client
import time


class RedisRepository:
    @staticmethod
    def set_task(task_id: str, task_status: dict):
        redis_client.set(task_id, json.dumps(task_status))

    @staticmethod
    def get_task(task_id: str):
        task_status = redis_client.get(task_id)
        if task_status:
            return json.loads(task_status)
        return None

    @staticmethod
    def push_task_to_queue(task: dict):
        redis_client.rpush("task_queue", json.dumps(task))

    @staticmethod
    def pop_task_from_queue():
        while True:
            redis_client.watch("task_queue")
            task_data = redis_client.lindex("task_queue", 0)
            if task_data:
                task = json.loads(task_data)
                task_id = task["task_id"]
                date = task["date"]
                supid = task["supid"]
                lock_key = f"lock:{task_id}:{date}:{supid}"
                if redis_client.setnx(lock_key, "locked"):
                    pipe = redis_client.pipeline()
                    pipe.lpop("task_queue")
                    pipe.execute()
                    redis_client.unwatch()
                    return task
            redis_client.unwatch()
            time.sleep(1)
        # _, task_data = redis_client.blpop("task_queue")
        # return json.loads(task_data) if task_data else None

    @staticmethod
    def lock_task(task_id: str, date: str, supid: int) -> bool:
        lock_key = f"lock:{task_id}:{date}:{supid}"
        return redis_client.setnx(lock_key, "locked")

    @staticmethod
    def unlock_task(task_id: str, date: str, supid: int):
        lock_key = f"lock:{task_id}:{date}:{supid}"
        redis_client.delete(lock_key)
