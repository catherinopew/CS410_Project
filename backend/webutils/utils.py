import hashlib
from datetime import datetime, timezone

# Tuple of students' unique identifiers
UIDs = ('as99', 'romanov2', 'bui5', 'jlo10', 'vdara2')

# Function to calculate MD5 hash for a given input string
def calculate_md5_hash(input_string):
    md5_hash = hashlib.md5()

    md5_hash.update(input_string.encode('utf-8'))
    md5_hash_hex = md5_hash.hexdigest()

    return md5_hash_hex

# Function to check if a request includes all required keys based on request type
def includes_all_keys(data, req_type='send_request'):
    # Define keys based on request type
    if req_type == 'send_request':
        keys = ('client_id', 'url', 'reviews')
    else:
        keys = ('client_id', 'task_id',)

    # Check if all keys are present in the request
    if all(k in data.keys() for k in keys):
        return True
    else:
        return False

# Function to get the current UTC timestamp in different formats (milli, micro, or seconds)
def get_utc_timestamp(format='milli'):
    # Define conversion factor based on the desired format
    if format == 'milli':
        k = 1e3
    elif format == 'micro':
        k = 1e6
    else:
        k = 1

    # Get the current UTC time and convert it to the specified format
    current_utc_time = datetime.now(timezone.utc)
    timestamp = int(current_utc_time.timestamp() * k)

    return timestamp

# Function to generate a task ID based on client ID and timestamp
def gen_task_id(client_id, timestamp):
    # Concatenate client ID and timestamp to create an input string
    input_string = str(client_id) + str(timestamp)
    
    # Calculate MD5 hash for the input string
    return calculate_md5_hash(input_string)
