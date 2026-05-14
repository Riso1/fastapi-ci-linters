import logging
import random
import threading
import time
from typing import List

INITIAL_TICKETS: int = 10
TOTAL_SEATS: int = 20
PRINT_BATCH: int = 6
SELLERS_COUNT: int = 4

AVAILABLE_TICKETS: int = INITIAL_TICKETS
SOLD_TICKETS: int = 0

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info(f"Seller {self.name} started work")

    def run(self) -> None:
        global AVAILABLE_TICKETS, SOLD_TICKETS

        while True:
            self.random_sleep()

            with self.sem:
                if SOLD_TICKETS >= TOTAL_SEATS:
                    break

                if AVAILABLE_TICKETS <= 0:
                    continue

                AVAILABLE_TICKETS -= 1
                SOLD_TICKETS += 1
                self.tickets_sold += 1

                logger.info(
                    f"{self.name} sold one ticket; "
                    f"available: {AVAILABLE_TICKETS}, sold: {SOLD_TICKETS}"
                )

        logger.info(f"Seller {self.name} sold {self.tickets_sold} tickets")

    def random_sleep(self) -> None:
        time.sleep(random.uniform(0.1, 0.8))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        logger.info("Director started work")

    def run(self) -> None:
        global AVAILABLE_TICKETS, SOLD_TICKETS

        while True:
            time.sleep(random.uniform(0.1, 0.5))

            with self.sem:
                if SOLD_TICKETS >= TOTAL_SEATS:
                    break

                remaining_capacity = TOTAL_SEATS - SOLD_TICKETS - AVAILABLE_TICKETS

                if remaining_capacity <= 0:
                    continue

                if 0 < AVAILABLE_TICKETS <= SELLERS_COUNT or AVAILABLE_TICKETS == 0:
                    new_tickets = min(PRINT_BATCH, remaining_capacity)
                    AVAILABLE_TICKETS += new_tickets

                    logger.info(
                        f"Director printed {new_tickets} tickets; "
                        f"available: {AVAILABLE_TICKETS}, sold: {SOLD_TICKETS}"
                    )

        logger.info("Director finished work")


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore(1)

    director = Director(semaphore)
    sellers: List[Seller] = []

    director.start()

    for _ in range(SELLERS_COUNT):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()

    director.join()

    logger.info(
        f"Work finished. Sold tickets: {SOLD_TICKETS}, "
        f"tickets left: {AVAILABLE_TICKETS}"
    )


if __name__ == '__main__':
    main()