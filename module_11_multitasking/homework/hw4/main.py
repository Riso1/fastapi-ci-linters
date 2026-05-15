import random
import time
from dataclasses import dataclass, field
from queue import PriorityQueue
from threading import Thread
from typing import Any, Callable


@dataclass(order=True)
class Task:
    priority: int
    func: Callable[..., Any] = field(compare=False)
    args: tuple[Any, ...] = field(compare=False, default_factory=tuple)

    def run(self) -> Any:
        return self.func(*self.args)

    def __repr__(self) -> str:
        return f"Task(priority={self.priority})"


def sleep_task(duration: float) -> None:
    print(f"sleep({duration})")
    time.sleep(duration)


class Producer(Thread):
    def __init__(self, task_queue: PriorityQueue, tasks_count: int = 10) -> None:
        super().__init__()
        self.task_queue = task_queue
        self.tasks_count = tasks_count

    def run(self) -> None:
        print("Producer: Running")

        for _ in range(self.tasks_count):
            priority = random.randint(0, 6)
            duration = random.random()
            task = Task(priority=priority, func=sleep_task, args=(duration,))
            self.task_queue.put(task)

        print("Producer: Done")


class Consumer(Thread):
    def __init__(self, task_queue: PriorityQueue) -> None:
        super().__init__()
        self.task_queue = task_queue

    def run(self) -> None:
        print("Consumer: Running")

        while not self.task_queue.empty():
            task: Task = self.task_queue.get()
            print(f">running {task}.", end="          ")
            task.run()
            self.task_queue.task_done()

        print("Consumer: Done")


def main() -> None:
    task_queue: PriorityQueue = PriorityQueue()

    producer = Producer(task_queue=task_queue, tasks_count=10)
    consumer = Consumer(task_queue=task_queue)

    producer.start()
    producer.join()

    consumer.start()
    consumer.join()

    task_queue.join()


if __name__ == "__main__":
    main()