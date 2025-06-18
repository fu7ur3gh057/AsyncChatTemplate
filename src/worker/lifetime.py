from taskiq_redis import ListQueueBroker


async def init_worker(broker: ListQueueBroker) -> None:
    if not broker.is_worker_process:
        await broker.startup()


async def shutdown_worker(broker: ListQueueBroker) -> None:
    if not broker.is_worker_process:
        await broker.shutdown()
