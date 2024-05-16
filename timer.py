import os
import re
import time
import sys
from datetime import datetime, timedelta

LOG_FOLDER = "log"

def ensure_log_folder_exists():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

def save_end_time(end_time, timer_name):
    ensure_log_folder_exists()
    file_path = os.path.join(LOG_FOLDER, f"{timer_name}.txt")
    with open(file_path, "w") as f:
        f.write(str(end_time))

def load_end_time(timer_name):
    file_path = os.path.join(LOG_FOLDER, f"{timer_name}.txt")
    try:
        with open(file_path, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return None

def parse_duration(duration_str):
    duration_regex = re.compile(r'(?:(\d+)y\s*)?(?:(\d+)mo\s*)?(?:(\d+)d\s*)?(?:(\d+)h\s*)?(?:(\d+)m\s*)?(?:(\d+)s\s*)?')
    matches = duration_regex.match(duration_str)
    if matches:
        years = int(matches.group(1) or 0)
        months = int(matches.group(2) or 0)
        days = int(matches.group(3) or 0)
        hours = int(matches.group(4) or 0)
        minutes = int(matches.group(5) or 0)
        seconds = int(matches.group(6) or 0)
        return timedelta(days=years*365 + months*30 + days, hours=hours, minutes=minutes, seconds=seconds)
    else:
        raise ValueError("Invalid duration format")

def format_time(delta):
    years, remainder = divmod(delta.days, 365)
    months, days = divmod(remainder, 30)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if years > 0:
        parts.append(f"{years} years")
    if months > 0:
        parts.append(f"{months} months")
    if days > 0:
        parts.append(f"{days} days")
    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0:
        parts.append(f"{minutes} minutes")
    parts.append(f"{seconds} seconds")
    return ", ".join(parts)

def countdown(end_time):
    while True:
        current_time = datetime.now().timestamp()
        if current_time >= end_time:
            print("Countdown finished!")
            break

        remaining_time = timedelta(seconds=end_time - current_time)
        time_str = format_time(remaining_time)
        print("\033[1;33;40m{}\033[0;0m".format(time_str), end="\r")
        sys.stdout.flush()

        time.sleep(1)

def start_new_timer():
    timer_name = input("Enter timer name: ")
    countdown_duration_str = input("Enter countdown duration (e.g., 2h 23m 34s): ")
    try:
        countdown_duration = parse_duration(countdown_duration_str)
        end_time = (datetime.now() + countdown_duration).timestamp()
        save_end_time(end_time, timer_name)
        print("Starting countdown with end time:", datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"))
        countdown(end_time)
    except ValueError as e:
        print("Error:", e)

def see_existing_timers():
    log_files = os.listdir(LOG_FOLDER)
    if not log_files:
        print("No existing timers found.")
        return

    print("Existing timers:")
    for index, log_file in enumerate(log_files, start=1):
        print(f"{index}. {os.path.splitext(log_file)[0]}")
    
    selected_index = int(input("Enter the index of the timer to see: "))
    selected_timer = log_files[selected_index - 1]
    timer_name = os.path.splitext(selected_timer)[0]
    end_time = load_end_time(timer_name)
    if end_time is None:
        print("Timer not found.")
        return
    print(f"End time for timer '{timer_name}':", datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"))
    countdown(end_time)

def main():
    ensure_log_folder_exists()
    if not os.listdir(LOG_FOLDER):
        print("No existing timers found.")
        start_new_timer()
    else:
        print("1. Start a new timer")
        print("2. See existing timers")
        choice = input("Enter your choice: ")
        if choice == "1":
            start_new_timer()
        elif choice == "2":
            see_existing_timers()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
