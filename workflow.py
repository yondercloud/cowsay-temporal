import asyncio
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from cowsay import cowsay
import os


@activity.defn
async def say(message: str) -> str:
    return cowsay(message)


@workflow.defn
class CowsayWorkflow:
    @workflow.run
    async def run(self, message: str) -> str:
        return await workflow.execute_activity(
            say,
            message,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def create_worker():
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    client = await Client.connect(temporal_host)
    worker = Worker(
        client,
        task_queue="cowsay-task-queue",
        workflows=[CowsayWorkflow],
        activities=[say],
    )
    return worker


if __name__ == "__main__":
    async def main():
        worker = await create_worker()
        print("Worker started. Listening for tasks...")
        await worker.run()

    asyncio.run(main())