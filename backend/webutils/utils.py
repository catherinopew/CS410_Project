import hashlib

from datetime import datetime, timezone


UIDs = ('as99', 'romanov2', 'bui5', 'jlo10', 'vdara2')

def calculate_md5_hash(input_string):
    md5_hash = hashlib.md5()

    md5_hash.update(input_string.encode('utf-8'))
    md5_hash_hex = md5_hash.hexdigest()

    return md5_hash_hex


def includes_all_keys(data, req_type='send_request'):
    if req_type == 'send_request':
        keys = ('client_id', 'url', 'reviews')
    else:
        keys = ('client_id', 'task_id',)

    if all(k in data.keys() for k in keys):
        return True
    else:
        return False

def get_utc_timestamp(format='milli'):
    if format == 'milli':
        k = 1e3
    elif format == 'micro':
        k = 1e6
    else:
        k = 1

    current_utc_time = datetime.now(timezone.utc)
    timestamp = int(current_utc_time.timestamp() * k)

    return timestamp

def gen_task_id(client_id, timestamp):
    input_string = str(client_id) + str(timestamp)
    return calculate_md5_hash(input_string)

