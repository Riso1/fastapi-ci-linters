import time
import requests
from threading import Thread
from queue import PriorityQueue


class Worker(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        start_time = time.time()
        while time.time() - start_time < 20:
            current_timestamp = int(time.time())
            date_string = get_date_from_server(current_timestamp)
            if date_string is not None:
                log_line = f"{current_timestamp} {date_string}"
                self.queue.put((current_timestamp, log_line))
            time.sleep(1)

class Writer(Thread):
    def __init__(self, queue, filename):
        super().__init__()
        self.queue = queue
        self.filename = filename

    def run(self):
        with open(self.filename, "a", encoding="utf-8") as file:
            while True:
                item = self.queue.get()
                timestamp, log_line = item
                if log_line is not None:
                    file.write(log_line + "\n")
                    file.flush()
                else:
                    break


def get_date_from_server(timestamp):
    url = f"http://127.0.0.1:8080/timestamp/{timestamp}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

if __name__ == "__main__":
    queue = PriorityQueue()
    filename = "logs.txt"

    open(filename, "w", encoding="utf-8").close()

    writer = Writer(queue, filename)
    workers = []

    writer.start()

    for _ in range(10):
        worker = Worker(queue)
        worker.start()
        workers.append(worker)
        time.sleep(1)

    for worker in workers:
        worker.join()
    queue.put((float("inf"), None))
    writer.join()