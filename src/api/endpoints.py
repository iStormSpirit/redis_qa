from fastapi import APIRouter, HTTPException
from src.services.task_service import TaskService

router = APIRouter()


@router.post("/start_task")
def start_task_calc(week_cnt: int, start_date: str = None):
    task_id = TaskService.start_task(week_cnt, start_date)
    return {"task_id": task_id}


@router.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task_status = TaskService.get_task_status(task_id)
    if not task_status:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return task_status
