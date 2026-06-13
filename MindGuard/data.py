import time

report_data = {
    "app_start_time": time.time(),

    "live_screen_time": "00:00:00",
    "screen_time": "0 mins",
    "usage_status": "Healthy usage",

    "stress_level": "Not Scanned",

    "reminder_enabled": False,
    "reminder_status": "No reminder set",
    "reminder_seconds": 0
}


def get_screen_time_seconds():
    return int(time.time() - report_data["app_start_time"])


def format_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_live_screen_time():
    seconds = get_screen_time_seconds()
    return format_seconds(seconds)


def get_today_usage():
    seconds = get_screen_time_seconds()
    minutes = seconds // 60
    return f"{minutes} mins"


def get_usage_status():
    seconds = get_screen_time_seconds()

    if seconds < 3600:
        return "Healthy usage"
    elif seconds < 7200:
        return "Moderate usage"
    else:
        return "High usage"