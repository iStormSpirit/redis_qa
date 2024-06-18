from pydantic import BaseModel
from typing import List, Dict, Union


class TaskStatus(BaseModel):
    status: str
    total: int
    done: int
    start_time: str
    end_time: Union[str, None]
    task: Dict[str, Union[str, int, None]]
    task_list: List[Dict[str, Union[str, int, None]]]
