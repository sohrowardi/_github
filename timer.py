import os
import re
import time
import sys

def save_end_time(end_time):
    with open("end_time.txt", "w") as f:
        f.write(str(end_time))

def load_end_time():
    try:
        with open("end_time.txt", "r") as f:
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
    # Check if there is a saved end time
    end_time = load_end_time()

    if end_time is None:
        # If no end time is saved, ask user to input the countdown duration
        countdown_duration_str = input("Enter countdown duration (e.g., 2h 23m 34s): ")
        print("Input received:", countdown_duration_str)
        try:
            countdown_duration = parse_duration(countdown_duration_str)
            end_time = int(time.time()) + countdown_duration
            print("End time:", end_time)
            save_end_time(end_time)
        except ValueError as e:
            print("Error:", e)
            return

    print("Starting countdown with end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    # Start countdown
    countdown(end_time)

if __name__ == "__main__":
    main()
