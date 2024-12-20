<!-- ![PyPI Version](https://img.shields.io/pypi/v/example-package) -->
<!-- ![Build Status](https://github.com/example-user/example-repo/actions/workflows/ci.yml/badge.svg) -->
<!-- ![Coverage](https://codecov.io/gh/example-user/example-repo/branch/main/graph/badge.svg) -->
![License](https://img.shields.io/github/license/Unobtainiumrock/parking-reminder)
![Stars](https://img.shields.io/github/stars/Unobtainiumrock/parking-reminder)
![Open Issues](https://img.shields.io/github/issues/Unobtainiumrock/parking-reminder)

# Car Reminder Script

This script periodically plays an audio reminder and displays a pop-up alert prompting you to move your car to avoid parking tickets. Users can dismiss the reminder by clicking a button, which disables further alerts until the next reset.

I cringe at all the AI voices these days, so I opted for espeak-ng's super robotic sounding voice with a British accent 😂

---

## Table of Contents

- [Car Reminder Script](#car-reminder-script)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
    - [Python Packages](#python-packages)
    - [External Dependencies](#external-dependencies)
      - [Install espeak-ng:](#install-espeak-ng)
    - [Ensure cron Is Installed and Running](#ensure-cron-is-installed-and-running)
      - [On Ubuntu:](#on-ubuntu)
      - [On macOS:](#on-macos)
  - [Setup](#setup)
  - [Example CLI Walkthrough](#example-cli-walkthrough)
  - [Crontab Syntax](#crontab-syntax)
    - [Basic Crontab Syntax](#basic-crontab-syntax)
    - [Using Logical AND in Crontab](#using-logical-and-in-crontab)
      - [Example Syntax Breakdown](#example-syntax-breakdown)
    - [Further Examples](#further-examples)
    - [How Logical AND (`-a`) and OR (`-o`) Work](#how-logical-and--a-and-or--o-work)
    - [Combining Multiple Conditions](#combining-multiple-conditions)
    - [Debugging Tips](#debugging-tips)
  - [Important Notes](#important-notes)

---

## Features

- **Configurable Reminders**: Users can specify their own reminder message and interval via command-line arguments.
- **Audio Reminders**: Uses espeak-ng for text-to-speech audio alerts.
- **Interactive Alert**: Displays a pop-up window with a "Dismiss Reminder" button to stop further reminders.

## Requirements

### Python Packages

- **tkinter**: Usually pre-installed with Python.
- **espeak-ng**: An external tool for text-to-speech.

### External Dependencies

**IMPORTANT NOTE**: I didn't run or test this on macOS, so you're on your own if things don't work out. I'll add better documentation and steps later for macOS if/when I feel like it.

#### Install espeak-ng:

```bash
# Ubuntu/Debian
sudo apt install espeak-ng

# macOS (via Homebrew)
brew install espeak-ng
```

### Ensure cron Is Installed and Running

Before proceeding, make sure cron is installed and running on your system.

#### On Ubuntu:

```bash
# Check if cron is installed
dpkg -l | grep cron

# Install cron if not installed
sudo apt update
sudo apt install cron

# Start and enable cron
sudo systemctl start cron
sudo systemctl enable cron

# Verify cron is running
sudo systemctl status cron
```

#### On macOS:

```bash
# Check if cron is installed and running
ps aux | grep cron

# If cron is not shown in the list, you may need to load it:
sudo launchctl load /System/Library/LaunchDaemons/com.vix.cron.plist

# Verify cron is loaded and running
launchctl list | grep cron
```

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Unobtainiumrock/parking-reminder.git
    cd parking-reminder
    ```

2. **Run the Setup Script**

    Use the provided `setup_cron.sh` to configure your cron jobs. This script will run the interactive `configure_cron.py` script to gather your preferences and set up the cron job accordingly. I suggest that during setup, you shift reminders to one day prior to the day that street cleaning is done.

    Make sure the script is executable:

    ```bash
    chmod +x setup_cron.sh
    ```

    Run the setup script:

    ```bash
    ./setup_cron.sh
    ```

## Example CLI Walkthrough

1. **Run the Setup Script:**

    ```bash
    ./setup_cron.sh
    ```

2. **Interactive CLI:**

    ```bash
    Welcome to the Cron Configuration for Parking Reminder!

    Enter the reminder message [Move your car to avoid a parking ticket!]: Please move your car to prevent a ticket.

    Select occurrences for reminders:
    1. First
    2. Second
    3. Third
    4. Fourth
    Enter the numbers corresponding to your choices (e.g., 1,3): 1,3

    Select days of the week for reminders:
    0. Sunday
    1. Monday
    2. Tuesday
    3. Wednesday
    4. Thursday
    5. Friday
    6. Saturday
    Enter the numbers corresponding to your choices (e.g., 1,3): 1,3

    Enter the reminder time (HH:MM, 24-hour format) [08:00]: 09:00

    How often do you want it to spam you to move your car, until you close the notification? (Measured in seconds.. yes I personally needed it in seconds) [5]: 10

    Cron jobs have been successfully configured!

    Resulting Cron Jobs: The script will set up cron jobs that trigger parking_reminder.py on:

      - 1st Monday: Days 1-7, Day of Week 1 (Monday).
      - 1st Wednesday: Days 1-7, Day of Week 3 (Wednesday).
      - 3rd Monday: Days 15-21, Day of Week 1 (Monday).
      - 3rd Wednesday: Days 15-21, Day of Week 3 (Wednesday).

    All at 09:00 AM with a spam interval of 10 seconds.

    **Once again, I strongly suggest setting them to the night or day prior. I learned this the hard way where I still didn't move my car in time. DONT BE ME**
    ```

## Crontab Syntax

### Basic Crontab Syntax

The crontab syntax defines how frequently a command or script should be executed. It has five fields followed by the command to execute:

```bash
* * * * * command_to_execute
| | | | |
| | | | +----- Day of the Week (0 - 7) (Sunday = 0 or 7)
| | | +------- Month (1 - 12)
| | +--------- Day of the Month (1 - 31)
| +----------- Hour (0 - 23)
+------------- Minute (0 - 59)
```

- `*` in any field means "every".
- A specific number indicates the exact value for that field (e.g., `5` in the hour field means 5 AM).
- Fields can also contain ranges (e.g., `1-5`), lists (e.g., `1,3,5`), and steps (e.g., `*/15` for every 15 minutes).

---

### Using Logical AND in Crontab

Crontab natively treats its fields as an "OR" within the range it matches. To add more complex logic, such as combining multiple conditions with logical AND, shell commands (e.g., `test` or `[ ... ]`) and operators like `-a` (AND) or `-o` (OR) are used in the script.

#### Example Syntax Breakdown

```bash
20 9 * * * [ "$(date +\%u)" -eq 5 -a "$(date +\%d)" -ge 8 -a "$(date +\%d)" -le 14 ] && /usr/bin/python3 /path/to/script.py
```

1. **Cron Time Fields (`20 9 * * *`):**
   - **Minute (20):** Run at the 20th minute.
   - **Hour (9):** Run at 9 AM.
   - **Day of Month (`*`):** No restriction; runs every day of the month.
   - **Month (`*`):** No restriction; runs every month.
   - **Day of Week (`*`):** No restriction; the script decides based on logic.

2. **Condition (`[ "$(date +\%u)" -eq 5 -a "$(date +\%d)" -ge 8 -a "$(date +\%d)" -le 14 ]`):**
   - This checks conditions before the script executes. If the condition evaluates to true, the script runs. If not, it doesn't execute.

   **Details of the Condition:**
   - `$(date +\%u)`: Retrieves the day of the week (1 = Monday, ..., 7 = Sunday).
     - `-eq 5`: Matches Friday (Day 5).
   - `$(date +\%d)`: Retrieves the day of the month.
     - `-ge 8`: Day is greater than or equal to 8.
     - `-le 14`: Day is less than or equal to 14.
   - `-a`: Logical AND operator; all conditions must be true.

   **Resulting Logic:**
   - The script will run only on Fridays when the date is between the 8th and the 14th of any month.

3. **Command (`&& /usr/bin/python3 /path/to/script.py`):**
   - If the condition evaluates as true, the `&&` ensures the script runs.

---

### Further Examples

1. **Saturday (Day 6) Between 8th and 14th:**

    ```bash
    20 9 * * * [ "$(date +\%u)" -eq 6 -a "$(date +\%d)" -ge 8 -a "$(date +\%d)" -le 14 ] && /usr/bin/python3 /path/to/script.py
    ```

    - Runs on Saturdays in the specified range of dates.

2. **Friday (Day 5) Between 22nd and 28th:**

    ```bash
    20 9 * * * [ "$(date +\%u)" -eq 5 -a "$(date +\%d)" -ge 22 -a "$(date +\%d)" -le 28 ] && /usr/bin/python3 /path/to/script.py
    ```

    - Runs on Fridays during the last full week of the month.

3. **Saturday (Day 6) Between 22nd and 28th:**

    ```bash
    20 9 * * * [ "$(date +\%u)" -eq 6 -a "$(date +\%d)" -ge 22 -a "$(date +\%d)" -le 28 ] && /usr/bin/python3 /path/to/script.py
    ```

    - Runs on Saturdays in the same date range.

---

### How Logical AND (`-a`) and OR (`-o`) Work

- **`-a` (AND):** Combines multiple conditions so all must be true for the command to execute.
  
  **Example:**

  ```bash
  [ "$(date +\%u)" -eq 5 -a "$(date +\%m)" -eq 12 ]
  ```

  - This runs only if it's Friday **AND** the month is December.

- **`-o` (OR):** At least one condition must be true.
  
  **Example:**

  ```bash
  [ "$(date +\%u)" -eq 5 -o "$(date +\%m)" -eq 12 ]
  ```

  - This runs if it's either Friday **OR** the month is December.

### Combining Multiple Conditions

For more complex logic:

```bash
[ "$(date +\%u)" -eq 5 -a "$(date +\%m)" -eq 12 -a "$(date +\%d)" -le 25 ]
```

- Runs only on Fridays in December before or on the 25th.

---

### Debugging Tips

To test the logic before adding it to crontab, run it directly in the terminal:

```bash
[ "$(date +%u)" -eq 5 -a "$(date +%d)" -ge 8 -a "$(date +%d)" -le 14 ] && echo "Condition matches!"
```

Replace the `echo` command with your script path once confirmed.

---

## Important Notes

- **macOS Compatibility:** I didn't run or test this on macOS, so you're on your own if things don't work out. I'll add better documentation and steps later for macOS if/when I feel like it.
  
- **Personal Advice:** Once again, I strongly suggest setting reminders to the night or day prior. I learned this the hard way where I still didn't move my car in time. **DONT BE ME**

---

