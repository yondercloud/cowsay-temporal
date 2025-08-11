import argparse
import asyncio
import uvicorn
from workflow import create_worker


async def run_worker():
    worker = await create_worker()
    print("Worker started. Listening for tasks on task queue: cowsay-task-queue")
    await worker.run()


def run_api():
    uvicorn.run("server:app", host="0.0.0.0", port=8000)


def main():
    parser = argparse.ArgumentParser(description="Cowsay Temporal Application")
    parser.add_argument(
        "--mode",
        choices=["api", "worker"],
        required=True,
        help="Run mode: api server or worker"
    )
    
    args = parser.parse_args()
    
    if args.mode == "api":
        run_api()
    elif args.mode == "worker":
        asyncio.run(run_worker())


if __name__ == "__main__":
    main()