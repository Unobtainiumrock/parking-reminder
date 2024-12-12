# Car Reminder Script

This script periodically plays an audio reminder and displays a pop-up alert prompting you to move your car to avoid parking tickets. Users can dismiss the reminder by clicking a button, which disables further alerts until the next reset.

I cringe at all the AI voices these days, so I opted for `espeak-ng`'s super robotic sounding voice with a British accent 😂

## Features
- **Configurable Reminders**: Users can specify their own reminder message and interval via command-line arguments.
- **Audio Reminders**: Uses `espeak-ng` for text-to-speech audio alerts.
- **Interactive Alert**: Displays a pop-up window with a "Dismiss Reminder" button to stop further reminders.

## Requirements

### Python Packages
- **tkinter**: Usually pre-installed with Python.
- **espeak-ng**: An external tool for text-to-speech.

### External Dependencies

IMPORTANT NOTE: I didn't run or test this on macOS, so you're on your own if things don't work out. I'll add better documentation and steps later for mac if/when I feel like it.

Install `espeak-ng`:
```bash
# Ubuntu/Debian
sudo apt install espeak-ng

# macOS (via Homebrew)
brew install espeak-ng
```

### Ensure `cron` Is Installed and Running

Before proceeding, make sure `cron` is installed and running on your system.

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

# Example CLI Walkthrough

1. **Run the Setup Script:**

```bash
./setup_cron.sh
```

2. **Interactive CLI**:

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

```

Resulting Cron Jobs: The script will set up cron jobs that trigger `parking_reminder.py` on:

  - 1st Monday: Days 1-7, Day of Week 1 (Monday).
  - 1st Wednesday: Days 1-7, Day of Week 3 (Wednesday).
  - 3rd Monday: Days 15-21, Day of Week 1 (Monday).
  - 3rd Wednesday: Days 15-21, Day of Week 3 (Wednesday).

All at 09:00 AM with a spam interval of 10 seconds.

**Once again, I strongly suggest setting them to the night or day prior. I learned this the hard way where I still didn't move my car in time. DONT BE ME**

