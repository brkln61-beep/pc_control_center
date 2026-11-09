import psutil


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