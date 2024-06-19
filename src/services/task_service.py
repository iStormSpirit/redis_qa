from loguru import logger
import uuid
import datetime
from src.repositories.redis_repository import RedisRepository


class TaskService:

    @staticmethod
    def get_week_list(cnt_week: int, start_date: str = None) -> list:
        week_start = datetime.date.today()
        if start_date:
            week_start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        week_end = week_start - datetime.timedelta(weeks=cnt_week)
        cur_week = week_start
        week_list = []
        while cur_week > week_end:
            week_list.append(str(cur_week))
            cur_week -= datetime.timedelta(weeks=1)
        return week_list

    @staticmethod
    def get_arg_list(week_cnt: int, start_date: str = None) -> list:
        week_list = TaskService.get_week_list(week_cnt, start_date)
        sup_list = [x for x in range(37, 420)]
        args_list = [{"date": d0, "supid": i} for d0 in week_list for i in sup_list]

        return args_list

    @staticmethod
    def start_task(week_cnt: int, start_date: str = None) -> str:
        task_id = str(uuid.uuid4())
        start_time = datetime.datetime.now().isoformat()
        args_list = TaskService.get_arg_list(week_cnt, start_date)
        logger.debug(f"start taskid {task_id} for len: {len(args_list)}")
        task_status = {
            "status": "in-progress",
            "total": len(args_list),
            "done": 0,
            "start_time": start_time,
            "end_time": None,
            "task_list": [{"status": "pending", "date": arg["date"], "supid": arg["supid"], "start_time": None,
                           "end_time": None} for arg in args_list]
        }
        RedisRepository.set_task(task_id, task_status)

        for arg in args_list:
            task = {"task_id": task_id, "date": arg["date"], "supid": arg["supid"]}
            RedisRepository.push_task_to_queue(task)

        return task_id

    @staticmethod
    def get_task_status(task_id: str) -> dict:
        return RedisRepository.get_task(task_id)

    @staticmethod
    def update_task_status(task_id: str, date: str, supid: int, status: str, start_time: str = None,
                           end_time: str = None):
        task_status = RedisRepository.get_task(task_id)
        logger.info(f"update task {task_id}, "
                    f"supid {supid} "
                    f"date {date} "
                    f"status {status} "
                    f"start time {start_time} "
                    f"end time {end_time}")

        if task_status:
            for t in task_status["task_list"]:
                if t["date"] == date and t["supid"] == supid:
                    t["status"] = status
                    if start_time:
                        t["start_time"] = start_time
                    if end_time:
                        t["end_time"] = end_time
            task_status["done"] += 1 if status == "completed" else 0
            if task_status["done"] == task_status["total"]:
                task_status["status"] = "completed"
                task_status["end_time"] = end_time
            RedisRepository.set_task(task_id, task_status)
