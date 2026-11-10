import psutil
import platform
import socket
from pathlib import Path
import time

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def get_cpu_cores():
    cores = psutil.cpu_percent(interval=1, percpu=True)
    return cores

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    disk = psutil.disk_usage("/")
    used_gb = disk.used / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)
    return disk.percent, used_gb, free_gb

def get_boot_time():
    boot_time = psutil.boot_time()
    return boot_time

def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "uptime": int(time.time() - psutil.boot_time()),
        "cpu": get_cpu_model(),
        "cpu_cores": psutil.cpu_count(logical=True),
        "ram_total": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }

def get_cpu_model():
    try:
        cpu_info = Path("/proc/cpuinfo").read_text()
        for line in cpu_info.splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass

    return platform.processor() or "Unknown"

def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    return f"{days} дн. {hours} ч. {minutes} мин."