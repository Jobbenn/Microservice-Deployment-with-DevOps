from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import add_task_to_user, move_task_for_user, get_user_kanban

kanban_bp = Blueprint('kanban', __name__)

@kanban_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task = request.json.get('task')
    add_task_to_user(current_user.id, task)
    return jsonify(get_user_kanban(current_user.id))

@kanban_bp.route('/move_task', methods=['POST'])
@login_required
def move_task():
    task = request.json.get('task')
    from_section = request.json.get('from')
    to_section = request.json.get('to')
    move_task_for_user(current_user.id, task, from_section, to_section)
    return jsonify(get_user_kanban(current_user.id))
