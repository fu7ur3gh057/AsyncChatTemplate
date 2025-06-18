import taskiq_fastapi
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisScheduleSource, RedisAsyncResultBackend

from src.core.settings import settings

broker = ListQueueBroker(
    settings.taskiq_broker_url, queue_name="taskiq:req"
).with_result_backend(RedisAsyncResultBackend(settings.taskiq_result_backend_url))
redis_source = RedisScheduleSource(settings.taskiq_broker_url)
scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])
taskiq_fastapi.init(broker, "src.web.application:get_app")


# @broker.task(task_name="add_one")
# async def add_one(value: int) -> int:
#     logging.info(f"Adding {value} to queue")
#     return value + 1
