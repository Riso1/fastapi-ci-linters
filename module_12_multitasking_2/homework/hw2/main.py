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

def process_exists(pid: int) -> bool:
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "pid="],
        capture_output=True,
        text=True
    )
    return bool(result.stdout.strip())

def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    if not process_exists(root_pid):
        raise ValueError(f"Process with PID {root_pid} not found.")

    all_pids = [root_pid]
    index = 0

    while index < len(all_pids):
        current_pid = all_pids[index]
        children = get_child_pids(current_pid)
        all_pids.extend(children)
        index += 1

    total_rss = 0.0
    for pid in all_pids:
        total_rss += get_rss_memory(pid)

    total_memory_kb = get_total_memory_kb()
    return round((total_rss / total_memory_kb) * 100, 2)

def get_child_pids(pid: int) -> list[int]:
    result = subprocess.run(
        ["pgrep", "-P", str(pid)],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return []

    return [int(x) for x in result.stdout.split()]

def get_rss_memory(pid: int) -> float:
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "rss="],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return 0.0

    return float(result.stdout.strip())

def get_total_memory_kb() -> float:
    result = subprocess.run(
        ["free", "-k"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()
    memory_line = lines[1].split()
    return float(memory_line[1])
