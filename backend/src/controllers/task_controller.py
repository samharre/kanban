from flask import Blueprint, request, jsonify, abort
from ..auth.auth import requires_auth, get_user_id
from ..models.task import Task
from ..models.phase import Phase
from ..utils.task_utils import (
    reorder_tasks_same_phase,
    reorder_tasks_diff_phases
)
import sys

task_bp = Blueprint('task_controller', __name__)


def list_tasks():
    user_id = get_user_id()
    return Task.query.filter(Task.user_id == user_id).\
        order_by(Task.phase_id, Task.order).all()


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = list_tasks()

        return jsonify({
            'success': True,
            'tasks': [task.serialize() for task in tasks]
        })
    except Exception:
        print(sys.exc_info())
        abort(500)


@task_bp.route('/phases/<int:phase_id>/tasks', methods=['GET'])
def get_tasks_per_phase(phase_id):
    try:
        tasks = Task.query.filter(
            Task.phase_id == phase_id).order_by(Task.order).all()

        return jsonify({
            'success': True,
            'tasks': [task.serialize() for task in tasks]
        })
    except Exception:
        print(sys.exc_info())
        abort(500)


@task_bp.route('/tasks', methods=['POST'])
@requires_auth('post:tasks')
def create_task(jwt_payload):
    body = request.get_json()
    if not body:
        abort(400)

    phase_id = body.get('phase_id')
    title = body.get('title')
    if not (phase_id and title):
        abort(422)

    phase = Phase.query.get(phase_id)
    if not phase:
        abort(422)

    query = Task.query.filter(
        Task.phase_id == phase_id, Task.user_id == jwt_payload.get('sub'))
    order = query.count() + 1

    description = body.get('description')
    priority = body.get('priority')
    due_date = body.get('due_date')

    try:
        task = Task(
            phase_id=phase_id,
            title=title,
            order=order,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=jwt_payload['sub']
        )
        task.insert()
    except Exception:
        task.rollback()
        print(sys.exc_info())
        abort(500)

    return jsonify({
        'success': True,
        'task': task.serialize()
    })


@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
@requires_auth('patch:tasks')
def update_task(jwt_payload, task_id):
    body = request.get_json()
    if not body:
        abort(400)

    new_phase_id = body.get('phase_id')
    new_title = body.get('title')
    new_order = body.get('order')

    if ('phase_id' in body and not new_phase_id) \
            or ('title' in body and not new_title):
        abort(422)

    if new_phase_id and not new_order:
        abort(422)

    task = Task.query.get(task_id)
    if not task:
        abort(404)

    try:
        prev_phase_id = task.phase_id
        prev_order = task.order

        if 'phase_id' in body:
            task.phase_id = new_phase_id

        if 'title' in body:
            task.title = new_title

        if 'description' in body:
            task.description = body.get('description')

        if 'priority' in body:
            task.priority = body.get('priority')

        if 'due_date' in body:
            task.due_date = body.get('due_date')

        tasks = []
        if (new_order and new_order != prev_order) \
                or (new_phase_id and new_phase_id != prev_phase_id):
            task.order = new_order

            if (new_phase_id and new_phase_id != prev_phase_id):
                tasks = reorder_tasks_diff_phases(
                    prev_phase_id=prev_phase_id,
                    new_phase_id=new_phase_id,
                    task_id=task.id,
                    order_prev_phase=prev_order,
                    order_new_phase=new_order
                )
            else:
                tasks = reorder_tasks_same_phase(
                    phase_id=prev_phase_id,
                    task_id=task.id,
                    prev_order=prev_order,
                    new_order=new_order
                )

            for task_reorderd in tasks:
                task.add_task_to_session(task_reorderd)

    except Exception:
        task.rollback()
        print(sys.exc_info())
        abort(500)
    else:
        task.commit()

    tasks = list_tasks()

    return jsonify({
        'success': True,
        'task': task.serialize(),
        'tasks': [task.serialize() for task in tasks]
    })


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@requires_auth('delete:tasks')
def delete_task(jwt_payload, task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)

    try:
        prev_order = task.order
        task.delete()

        tasks = reorder_tasks_same_phase(
            phase_id=task.phase_id,
            task_id=task.id,
            prev_order=prev_order,
            new_order=None
        )

        for task_reorderd in tasks:
            task.add_task_to_session(task_reorderd)

    except Exception:
        task.rollback()
        print(sys.exc_info())
        abort(500)

    return jsonify({
        'success': True,
        'task_deleted': task_id
    })
