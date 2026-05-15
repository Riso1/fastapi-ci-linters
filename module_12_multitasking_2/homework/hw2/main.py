import subprocess

def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    command = f"ps -u {username} -o pid= | wc -l"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    all_pids = [root_pid]
    index = 0

    while index < len(all_pids):
        current_pid = all_pids[index]
        children = get_child_pids(current_pid)
        all_pids.extend(children)
        index += 1

    total_memory = 0.0
    for pid in all_pids:
        total_memory += get_memory_usage(pid)

    return total_memory

def get_child_pids(pid: int) -> list[int]:
    result = subprocess.run(
        ["pgrep", "-P", str(pid)],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return []

    return [int(x) for x in result.stdout.split()]

def get_memory_usage(pid: int) -> float:
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "%mem="],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return 0.0

    return float(result.stdout.strip())
