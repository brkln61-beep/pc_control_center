from pathlib import Path


def read_sensor_value(file_path):
    try:
        value = Path(file_path).read_text().strip()
        return int(value) / 1000
    except (OSError, ValueError):
        return None

def read_sensor_label(file_path):
    try:
        return Path(file_path).read_text().strip()
    except OSError:
        return None

def get_hwmon_devices():
    hwmon_path = Path("/sys/class/hwmon/")

    if not hwmon_path.exists():
        return []

    return sorted(hwmon_path.glob("hwmon*"))

def get_sensor_name(device_path):
    name_file = device_path / "name"
    return read_sensor_label(name_file)

def get_device_temperatures(device_path):
    sensors = []

    for temp_file in sorted(device_path.glob("temp*_input")):
        temperature = read_sensor_value(temp_file)

        if temperature is None:
            continue

        sensor_prefix = temp_file.name.replace("_input", "")

        label_file = temp_file.with_name(
            f"{sensor_prefix}_label"
        )

        max_file = temp_file.with_name(
            f"{sensor_prefix}_max"
        )

        crit_file = temp_file.with_name(
            f"{sensor_prefix}_crit"
        )

        label = read_sensor_label(label_file)

        if label is None:
            label = sensor_prefix

        max_temp = read_sensor_value(max_file)
        critical_temp = read_sensor_value(crit_file)

        status = get_temperature_status(
            temperature,
            max_temp,
            critical_temp
        )

        sensors.append({
            "label": label,
            "temperature": temperature,
            "max": max_temp,
            "critical": critical_temp,
            "status": status
        })

    return sensors

def get_all_temperatures():
    devices = []

    for device_path in get_hwmon_devices():
        device_name = get_sensor_name(device_path)
        temperatures = get_device_temperatures(device_path)

        if not temperatures:
            continue

        devices.append({
            "device": device_name,
            "sensors": temperatures
        })

    return devices

def get_temperature_status(temperature, max_temp=None, critical_temp=None):
    if critical_temp is not None and temperature >= critical_temp:
        return "critical"

    if max_temp is not None and temperature >= max_temp:
        return "warning"

    return "normal"