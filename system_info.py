
import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_available_ram():
    memory = psutil.virtual_memory()
    return round(memory.available / (1024**3), 2)

def get_battery():
    battery = psutil.sensors_battery()

    if battery:
        return battery.percent

    return None
