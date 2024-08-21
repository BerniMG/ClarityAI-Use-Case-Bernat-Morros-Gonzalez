import datetime

def parse_log_line(line):
    """Parse a single line of the log file and return the timestamp, source host, and destination host."""
    parts = line.strip().split()  # Split the line into components
    
    if len(parts) != 3:
        raise ValueError(f"Malformed log line: {line}")  # Ensure line has exactly 3 parts

    unix_timestamp_str, source_host, destination_host = parts  # Assign the parts to variables
    
    try:
        unix_timestamp = int(unix_timestamp_str) // 1000  # Convert timestamp from milliseconds to seconds
    except ValueError:
        raise ValueError(f"Invalid timestamp: {unix_timestamp_str}")  # Handle invalid timestamp
    
    # Validate the timestamp
    if unix_timestamp < 0:
        raise ValueError(f"Negative timestamp: {unix_timestamp_str}")  # Check for negative timestamps
    
    current_time = int(datetime.datetime.utcnow().timestamp())  # Get current UTC timestamp
    
    # Ensure the timestamp is within a logical range (last 50 years and not in the future)
    if unix_timestamp > current_time or unix_timestamp < current_time - 50 * 365 * 24 * 3600:
        raise ValueError(f"Timestamp out of logical range: {unix_timestamp_str}")
    
    return unix_timestamp, source_host, destination_host  # Return parsed components

def find_date_range(log_file_path):
    """Find the minimum and maximum timestamps in the log file."""
    min_timestamp = float('inf')  # Initialize with the highest possible value
    max_timestamp = float('-inf')  # Initialize with the lowest possible value
    
    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                unix_timestamp, _, _ = parse_log_line(line)  # Parse each line and extract the timestamp
                min_timestamp = min(min_timestamp, unix_timestamp)  # Track the minimum timestamp
                max_timestamp = max(max_timestamp, unix_timestamp)  # Track the maximum timestamp
            except ValueError as e:
                print(f"Error processing line: {line} - {e}")  # Handle any parsing errors
    
    if min_timestamp == float('inf') or max_timestamp == float('-inf'):
        return None, None  # Return None if no valid timestamps were found
    
    min_datetime = datetime.datetime.utcfromtimestamp(min_timestamp)  # Convert min timestamp to datetime
    max_datetime = datetime.datetime.utcfromtimestamp(max_timestamp)  # Convert max timestamp to datetime
    
    return min_datetime, max_datetime  # Return the min and max datetimes

def is_timestamp_in_range(log_time, start_time, end_time):
    """Check if the log time is within the specified range."""
    return start_time <= log_time <= end_time  # Return True if log_time is within the range

def add_connection(connections, source_host, destination_host, target_hostname):
    """Add the source host to the connection list if it connects to the target hostname."""
    if destination_host == target_hostname:
        connections.add(source_host)  # Add source_host if destination matches target

def filter_connections(log_file_path, start_datetime_str, end_datetime_str, target_hostname):
    """Filter connections from the log file based on the specified time range and target hostname."""
    
    start_datetime_str = start_datetime_str.strip()  # Remove leading/trailing spaces from start time
    end_datetime_str = end_datetime_str.strip()  # Remove leading/trailing spaces from end time
    
    start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")  # Parse start time
    end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")  # Parse end time
    
    connections = set()  # Initialize an empty set to store connections
    
    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                unix_timestamp, source_host, destination_host = parse_log_line(line)  # Parse log line
                
                log_time = datetime.datetime.utcfromtimestamp(unix_timestamp)  # Convert timestamp to datetime
                
                if is_timestamp_in_range(log_time, start_datetime, end_datetime):
                    add_connection(connections, source_host, destination_host, target_hostname)  # Add connection if in range
                    
            except ValueError as e:
                print(f"Error processing line: {line} - {e}")  # Handle parsing errors
    
    return list(connections)  # Return the list of connections

def main():
    """Main function to execute the log filtering."""
    log_file_path = "input-file-10000__1_.txt"  # Path to the log file
    
    min_datetime, max_datetime = find_date_range(log_file_path)  # Determine the date range in the log file
    
    if min_datetime and max_datetime:
        print(f"The log file covers the period from {min_datetime} to {max_datetime}.")  # Print the date range
    else:
        print("No valid timestamps found in the log file.")
        return
    
    # Prompt the user for the start and end datetime within the found range
    start_datetime_str = input(f"Enter the start datetime (YYYY-MM-DD HH:MM:SS) within {min_datetime.strftime('%Y-%m-%d %H:%M:%S')} and {max_datetime.strftime('%Y-%m-%d %H:%M:%S')}: ")
    end_datetime_str = input(f"Enter the end datetime (YYYY-MM-DD HH:MM:SS) within {min_datetime.strftime('%Y-%m-%d %H:%M:%S')} and {max_datetime.strftime('%Y-%m-%d %H:%M:%S')}: ")
    
    target_hostname = input("Enter the target hostname: ")  # Prompt for the target hostname
    
    connected_hosts = filter_connections(log_file_path, start_datetime_str, end_datetime_str, target_hostname)  # Filter connections
    
    # Print the list of hosts connected to the target during the specified period
    print(f"Hosts connected to {target_hostname} during the period {start_datetime_str} to {end_datetime_str}:")
    print(connected_hosts)

if __name__ == "__main__":
    main()  # Execute the main function
