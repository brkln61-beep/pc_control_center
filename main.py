from core.system_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_cpu_cores, get_boot_time
from datetime import datetime

print("=== PC CONTROL CENTER ===")
now = datetime.now()
print(now.strftime("%d.%m.%Y %H:%M:%S"))

cpu = get_cpu_usage()
memory = get_memory_usage()
disk_percent, used_gb, free_gb = get_disk_usage()
cores = get_cpu_cores()
boot_time = get_boot_time()
boot_date = datetime.fromtimestamp(boot_time)
print(boot_date)
uptime = datetime.now() - boot_date
print(f"Uptime: {uptime.days} дней, {uptime.seconds // 3600} часов, {(uptime.seconds % 3600) // 60} минут, {uptime.seconds % 60} секунд")

print(f"Процессор: {cpu}%")
print(f"Оперативная память: {memory}%")
print(f"Заполнение диска: {disk_percent}%")
print(f"Занято: {used_gb:.2f} ГБ")
print(f"Свободно: {free_gb:.2f} ГБ")

for number, usage in enumerate(cores, start=1):
    print(f"Ядро {number}: {usage:.2f}%")

print()
print("=== ПРОЦЕССОР ===")
if cpu <= 30:
    print("Низкая нагрузка")

elif cpu <= 70:
    print("Средняя загрузка")

else:
    print("Высокая нагрузка")

print()
print("=== ОПЕРАТИВНАЯ ПАМЯТЬ ===")
if memory <= 60:
    print("Оперативной памяти достаточно")

elif memory <= 85:
    print("Оперативная память используется активно")

else:
    print("Внимание! Высокая загрузка оперативной памяти")

print()
print("=== ЖЁСТКИЙ ДИСК ===")
if free_gb >= 50:
    print("Свободного места на диске достаточно")

elif free_gb >=20:
    print("Свободного места становится меньше")

else:
    print("Внимание! Мало свободного места на диске")
