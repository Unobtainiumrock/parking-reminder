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

import subprocess
import tkinter as tk
import argparse
from typing import NoReturn, Callable

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the reminder script.
    """
    parser = argparse.ArgumentParser(description="Car parking reminder script.")
    parser.add_argument(
        "--message",
        type=str,
        default="Hello! Move your car to avoid a parking ticket",
        help="Reminder message to be spoken and displayed."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Time interval (in seconds) between audio plays."
    )
    return parser.parse_args()

def play_reminder(msg: str) -> None:
    """
    Play the reminder message using espeak-ng.
    """
    subprocess.run(["espeak-ng", "-a", "10", "Wake up, Yi Lin"], check=True)
    subprocess.run(["espeak-ng", msg], check=True)

def schedule_audio(root: tk.Tk, 
                   msg: str, 
                   interval: int, 
                   running_check: Callable[[], bool]) -> None:
    """
    Schedule repeated audio playback inside the Tkinter event loop.
    Continues as long as running_check() returns True.
    """
    if running_check():
        play_reminder(msg)
        root.after(interval * 1000, schedule_audio, root, msg, interval, running_check)

def show_popup(msg: str, interval: int) -> None:
    """
    Displays a popup alert and schedules repeating audio reminders 
    until the user dismisses the popup.
    """
    root = tk.Tk()
    root.title("Reminder Alert")
    root.geometry("300x150")

    running = True
    
    def on_dismiss():
        nonlocal running
        running = False
        root.destroy()

    label = tk.Label(root, text=msg, wraplength=250)
    label.pack(pady=10)

    dismiss_button = tk.Button(root, text="Dismiss Reminder", command=on_dismiss)
    dismiss_button.pack(pady=10)

    # This function will keep returning True as long as the popup is running
    def is_running() -> bool:
        return running

    # Start the audio reminder loop
    schedule_audio(root, msg, interval, is_running)

    root.mainloop()

def main() -> NoReturn:
    args = parse_args()
    msg = args.message
    interval = args.interval

    # Show the popup and run the main loop for audio reminders
    show_popup(msg, interval)

if __name__ == "__main__":
    main()

