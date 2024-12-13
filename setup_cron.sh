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

# #!/bin/bash

# Determine the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 and try again."
    exit 1
fi

# Define the path to configure_cron.py
CRON_SCRIPT_PATH="parking_reminder/configure_cron.py"

# Check if configure_cron.py exists
if [ ! -f "$CRON_SCRIPT_PATH" ]; then
    echo "configure_cron.py not found in the expected directory: $CRON_SCRIPT_PATH."
    exit 1
fi

# Make configure_cron.py executable
chmod +x "$CRON_SCRIPT_PATH"

# Run the configuration script
echo "Running the cron configuration script..."
python3 "$CRON_SCRIPT_PATH"

echo "Cron setup completed."
