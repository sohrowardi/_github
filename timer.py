import os
import re
import time
import sys

def clear_terminal():
    # Clearing the terminal screen
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def save_end_time(end_time, timer_name):
    script_dir = os.path.dirname(__file__)
    log_folder = os.path.join(script_dir, "log")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    file_path = os.path.join(log_folder, f"{timer_name}.txt")
    with open(file_path, "w") as f:
        f.write(str(end_time))

def load_end_time(timer_name):
    script_dir = os.path.dirname(__file__)
    log_folder = os.path.join(script_dir, "log")
    file_path = os.path.join(log_folder, f"{timer_name}.txt")
    try:
        with open(file_path, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return None

def parse_duration(duration_str):
    duration_regex = re.compile(r'(?:(\d+)d\s*)?(?:(\d+)h\s*)?(?:(\d+)m\s*)?(?:(\d+)s\s*)?')
    matches = duration_regex.match(duration_str)
    if matches:
        days = int(matches.group(1) or 0)
        hours = int(matches.group(2) or 0)
        minutes = int(matches.group(3) or 0)
        seconds = int(matches.group(4) or 0)
        return days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds
    else:
        raise ValueError("Invalid duration format")

def format_time(days, hours, minutes, seconds):
    time_str = ""
    if days:
        time_str += f"{days} days, "
    if hours:
        time_str += f"{hours} hours, "
    if minutes:
        time_str += f"{minutes} minutes, "
    time_str += f"{seconds} seconds"
    return time_str

def countdown(end_time):
    while True:
        clear_terminal()  # Clearing the terminal before displaying the countdown
        current_time = int(time.time())
        if current_time >= end_time:
            print("Countdown finished!")
            break

        remaining_time = end_time - current_time
        minutes, seconds = divmod(remaining_time, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        time_str = format_time(days, hours, minutes, seconds)
        print("\033[1;33;40m{}\033[0;0m".format(time_str), end="\r")
        sys.stdout.flush()

        time.sleep(1)

def main():
    script_dir = os.path.dirname(__file__)
    log_folder = os.path.join(script_dir, "log")
    if not os.path.exists(log_folder) or not os.listdir(log_folder):
        print("No existing timers found.")
        timer_name = input("Enter timer name: ")
        countdown_duration_str = input("Enter countdown duration (e.g., 2h 23m 34s): ")
        print("Input received:", countdown_duration_str)
        try:
            countdown_duration = parse_duration(countdown_duration_str)
            end_time = int(time.time()) + countdown_duration
            print("End time:", end_time)
            save_end_time(end_time, timer_name)
        except ValueError as e:
            print("Error:", e)
            return
        print("Starting countdown with end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
        countdown(end_time)
    else:
        print("1. Start a new timer")
        print("2. See existing timers")
        choice = input("Enter your choice: ")
        if choice == "1":
            timer_name = input("Enter timer name: ")
            countdown_duration_str = input("Enter countdown duration (e.g., 2h 23m 34s): ")
            print("Input received:", countdown_duration_str)
            try:
                countdown_duration = parse_duration(countdown_duration_str)
                end_time = int(time.time()) + countdown_duration
                print("End time:", end_time)
                save_end_time(end_time, timer_name)
            except ValueError as e:
                print("Error:", e)
                return
            print("Starting countdown with end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
            countdown(end_time)
        elif choice == "2":
            log_files = os.listdir(log_folder)
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
            print(f"End time for timer '{timer_name}':", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
            countdown(end_time)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
