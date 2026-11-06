import psutil

print("=== PC CONTROL CENTER ===")

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage("/")

print(f"Процессор: {cpu}%")
print(f"Оперативная память: {memory.percent}%")
print(f"Всего RAM: {memory.total / (1024 ** 3):.2f} GB")
print(f"Занято на диске: {disk.percent}%")
print(f"Свободно на диске: {disk.free / (1024 ** 3):.2f} GB")
