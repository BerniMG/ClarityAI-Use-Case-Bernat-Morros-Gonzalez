# Log Connection Analyzer

This Python script is used to analyze a connection log file and filter connections to a specific host within a given date and time range.

## Features

- **Log Parsing:** Reads and parses each line of the log file to extract the timestamp, source host, and destination host.
- **Date Range Detection:** Finds the minimum and maximum timestamps in the log file, allowing the user to know the date range covered by the log.
- **Connection Filtering:** Filters connections that occurred within a specific date range and involved a user-defined target host.
- **Interactive Interface:** Prompts the user to input the date range and target hostname to perform the analysis.

## Requirements

- Python 3.x
- No additional external libraries are required

## Setup

1. **Install Pyenv:**

   Pyenv is a tool to manage multiple Python versions on your machine. You can install it using the following commands:

   ```bash
   curl https://pyenv.run | bash
   ```

   Follow the instructions to add Pyenv to your shell's configuration file (e.g., `.bashrc` or `.zshrc`).

   After installation, restart your shell and verify that Pyenv is installed:

   ```bash
   pyenv --version
   ```

2. **Install Python with Pyenv:**

   Use Pyenv to install a specific version of Python:

   ```bash
   pyenv install 3.x.x  # Replace with the desired Python version
   pyenv global 3.x.x    # Set the installed version as the global default
   ```

3. **Create a Python virtual environment:**

   Once you've set the Python version, you can create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. **Activate your virtual environment:**

   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .env\Scriptsctivate
     ```

5. **Install dependencies:**

   Although the script doesn't require external libraries, if you plan to extend it, you might want to manage dependencies through a `requirements.txt` file. Install any required dependencies with:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare the log file:** Ensure the log file is in the same directory as the script, or provide the full path to the file in the `log_file_path` variable within the script.

2. **Run the script:**

   You can execute the script from the command line or within a development environment:

   ```bash
   python log_analyzer.py
   ```

   The script will prompt you to input the following:
   - Start and end date-time range (format: `YYYY-MM-DD HH:MM:SS`)
   - The target hostname you want to analyze.

3. **View Results:**

   The script will display a list of hosts that connected to the target host during the specified period.

### Example Usage

```bash
$ python log_analyzer.py
```

During execution, the script asks for the following:

```
The log file covers the period from 2024-01-01 00:00:00 to 2024-12-31 23:59:59.
Enter the start datetime (YYYY-MM-DD HH:MM:SS) within 2024-01-01 00:00:00 and 2024-12-31 23:59:59: 2024-06-01 00:00:00
Enter the end datetime (YYYY-MM-DD HH:MM:SS) within 2024-01-01 00:00:00 and 2024-12-31 23:59:59: 2024-06-30 23:59:59
Enter the target hostname: Zyla
```

The script will generate a list of hosts connected to `Zyla` during June 2024.

## Code Structure

- `parse_log_line(line)`: Parses a line from the log file and returns the timestamp, source host, and destination host.
- `find_timestamp_range(log_file_path)`: Finds the minimum and maximum timestamps in the log file.
- `is_within_range(log_time, start_time, end_time)`: Checks if a timestamp is within a specified range.
- `add_connection(connections, source_host, destination_host, target_hostname)`: Adds the source host to the connection list if it connects to the target hostname.
- `filter_connections(log_file_path, start_datetime_str, end_datetime_str, target_hostname)`: Filters and returns the connections occurring within a date range for a target host.
- `main()`: The main function that runs the interactive log analysis.

## Considerations

- **Log File Format:** The log file should contain three columns: the Unix timestamp (in milliseconds), the source host, and the destination host. Each column should be separated by a space.
- **Error Handling:** The script handles possible format errors and incorrect values, informing the user with messages in the console.
