from flask import Blueprint, request, jsonify
from webutils.utils import *
from webutils import rmq_handler, db_handler

# Create a Flask Blueprint for the API
bp = Blueprint('api', __name__)

# Endpoint for handling POST requests to send requests
@bp.route('/send_request', methods=['POST'])
def request_handler():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    # Retrieve JSON data from the request
    data = request.get_json()

    # Check if the required keys are present in the JSON data
    if not includes_all_keys(data, req_type='send_request'):
        return jsonify({"status": "error", "message": f"Missing required keys"}), 400

    # Add timestamp and task_id to the data
    data['timestamp'] = get_utc_timestamp()
    data['task_id'] = gen_task_id(data['client_id'], data['timestamp'])

    # Insert the task into the database
    db_handler.insert_task(data)

    # Publish the message to RabbitMQ
    rc = rmq_handler.publish_message(data)

    # Return the response based on the result of publishing the message
    if rc['status'] == 'ok':
        return jsonify({'status': 'ok', 'message': {"task_id": data['task_id']}}), 200
    else:
        return jsonify({'status': 'error', 'message': f"{rc['status']}"}), 400

# Endpoint for handling POST requests to get responses
@bp.route('/get_response', methods=['POST'])
def response_handler():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    # Retrieve JSON data from the request
    data = request.get_json()

    # Check if the required keys are present in the JSON data
    if not includes_all_keys(data, req_type='get_response'):
        return jsonify({"status": "error", "message": f"Missing required keys"}), 400

    # Check the result in the database
    rc = db_handler.check_result(data)

    # Return the database query result as a JSON response
    return jsonify(rc)
