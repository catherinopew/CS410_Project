from flask import Blueprint, request, jsonify
from webutils.utils import *
from webutils import rmq_handler, db_handler

bp = Blueprint('api', __name__)

@bp.route('/send_request', methods=['POST'])
def request_handler():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    data = request.get_json()

    if not includes_all_keys(data, req_type='send_request'):
        return jsonify( {"status": "error", "message": f"Missing required keys"}), 400

    data['timestamp'] = get_utc_timestamp()
    data['task_id'] = gen_task_id(data['client_id'], data['timestamp'])

    db_handler.insert_task(data)
    rc = rmq_handler.publish_message(data)

    if rc['status'] == 'ok':
        return jsonify( {'status': 'ok', 'message': {"task_id": data['task_id']}}), 200
    else:
        return jsonify( {'status': 'error', 'message': f"{rc['status']}"}), 400


@bp.route('/get_response', methods=['POST'])
def response_handler():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    data = request.get_json()

    if not includes_all_keys(data, req_type='get_response'):
        return jsonify( {"status": "error", "message": f"Missing required keys"}), 400

    rc = db_handler.check_result(data)

    return jsonify(rc)
