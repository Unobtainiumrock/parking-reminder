# Copyright 2024 Nicholas Fleischhauer
# 
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.gnu.org/licenses/gpl-3.0.html
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
from typing import Dict, List, Optional

# Represents the n-th occurrence of a day in a given month.
OCCURRENCES: Dict[str, str] = {
    "1": "First",
    "2": "Second",
    "3": "Third",
    "4": "Fourth",
}

DAYS_OF_WEEK: Dict[str, str] = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
}

OCCURRENCE_RANGES: Dict[str, str] = {
    "1": "1-7",
    "2": "8-14",
    "3": "15-21",
    "4": "22-28",
}

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Prompt the user for input with an optional default value."""
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default

def select_options(options: Dict[str, str], prompt: str) -> List[str]:
    """
    Display a list of options and allow the user to select multiple choices.

    Args:
        options (Dict[str, str]): A dictionary where keys are option numbers and values are option descriptions.
        prompt (str): The prompt message to display.

    Returns:
        List[str]: A list of selected option keys as strings.
    """
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")
    selected = input("Enter the numbers corresponding to your choices (e.g., 1,3): ").split(",")
    selected = [s.strip() for s in selected if s.strip() in options]
    return selected

def configure_cron() -> None:
    """Configure cron jobs based on user input."""
    print("Welcome to the Cron Configuration for Parking Reminder!\n")
    
    # Get reminder message
    reminder_message = get_user_input(
        "Enter the reminder message", default="Move your car to avoid a parking ticket!"
    )
    
    # Select occurrences
    print("\nSelect occurrences for reminders:")
    selected_occurrences = select_options(OCCURRENCES, "Select the occurrences of the month for reminders:")
    
    if not selected_occurrences:
        print("No valid occurrences selected. Exiting.")
        return
    
    # Select days
    print("\nSelect days of the week for reminders:")
    selected_days = select_options(DAYS_OF_WEEK, "Select the days of the week for reminders:")
    
    if not selected_days:
        print("No valid days selected. Exiting.")
        return
    
    # Get reminder time
    while True:
        reminder_time = get_user_input("Enter the reminder time (HH:MM, 24-hour format)", default="08:00")
        try:
            hour, minute = map(int, reminder_time.split(":"))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                break
            else:
                print("Invalid time. Please enter a valid time in HH:MM format.")
        except ValueError:
            print("Invalid format. Please enter time as HH:MM.")
    
    # Get reminder interval in seconds
    while True:
        interval_input = get_user_input(
            "How often do you want it to spam you to move your car, until you close the notification? (Measured in seconds)", 
            default="5"
        )
        try:
            interval = int(interval_input)
            if interval > 0:
                break
            else:
                print("Interval must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer for the interval.")
    
    # Get the project directory
    project_dir = os.getcwd()
    
    # Initialize cron entries with environment variables
    env_vars = """\
DISPLAY=:0
WAYLAND_DISPLAY=wayland-0
XDG_RUNTIME_DIR=/run/user/$(id -u)
PULSE_SERVER=unix:/mnt/wslg/PulseServer
"""
    cron_entries = [env_vars]
    
    # Generate cron entries for each combination of occurrence and day
    for occ in selected_occurrences:
        day_range = OCCURRENCE_RANGES[occ]
        for day in selected_days:
            cron_entry = (
                f"{minute} {hour} {day_range} * {day} "
                f'[ "$(date +\\%d)" -ge {day_range.split("-")[0]} -a "$(date +\\%d)" -le {day_range.split("-")[1]} ] && '
                f"/usr/bin/python3 {project_dir}/parking_reminder.py --message \"{reminder_message}\" --interval {interval}"
            )
            cron_entries.append(cron_entry)
    
    # Combine the cron entries into a single string
    new_cron_jobs = "\n".join(cron_entries) + "\n"
    
    # Retrieve existing cron jobs
    try:
        existing_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        existing_cron = ""
    
    # Remove existing parking_reminder.py cron jobs and environment variables
    filtered_cron = "\n".join(
        line for line in existing_cron.split("\n") 
        if "parking_reminder.py" not in line and not any(env in line for env in ["DISPLAY=", "WAYLAND_DISPLAY=", "XDG_RUNTIME_DIR=", "PULSE_SERVER="])
    )
    
    # Combine existing cron with new cron entries
    updated_cron = filtered_cron.strip() + "\n" + new_cron_jobs
    
    # Update the crontab
    process = subprocess.run(["crontab"], input=updated_cron, text=True)
    
    if process.returncode == 0:
        print("\nCron jobs have been successfully configured!")
    else:
        print("\nAn error occurred while setting up cron jobs.")

if __name__ == "__main__":
    configure_cron()
