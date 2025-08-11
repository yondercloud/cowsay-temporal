import asyncio
from workflow import create_worker


if __name__ == "__main__":
    async def main():
        worker = await create_worker()
        print("Worker started. Listening for tasks on task queue: cowsay-task-queue")
        await worker.run()

    asyncio.run(main())