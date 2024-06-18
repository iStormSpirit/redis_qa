import json
from src.core.config import redis_client


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
        _, task_data = redis_client.blpop("task_queue")
        return json.loads(task_data) if task_data else None
