from flask import Blueprint, request, jsonify, abort
from ..auth.auth import requires_auth
from ..models.phase import Phase
from ..utils.phase_utils import reorder_phases, check_title_phase_exists
import sys

phase_bp = Blueprint('phase_controller', __name__)

@phase_bp.route('/phases', methods=['GET'])
def get_phases():
  try:
    phases = Phase.query.order_by(Phase.order).all()

    return jsonify({
      'success': True,
      'phases': [phase.serialize() for phase in phases]
    })
  except:
    print(sys.exc_info())
    abort(500)


@phase_bp.route('/phases/<int:phase_id>', methods=['GET'])
def get_phases_by_id(phase_id):
  # try:
    phase = Phase.query.get(phase_id)
    if not phase:
      abort(404)

    return jsonify({
      'success': True,
      'phase': phase.serialize()
    })
  # except:
  #   print(sys.exc_info())
  #   abort(500)


@phase_bp.route('/phases-detail', methods=['GET'])
def get_phases_detail():
  try:
    phases = Phase.query.order_by(Phase.order).all()

    return jsonify({
      'success': True,
      'phases': [phase.serialize_with_tasks() for phase in phases]
    })
  except:
    print(sys.exc_info())
    abort(500)


@phase_bp.route('/phases-detail/<int:phase_id>', methods=['GET'])
def get_phases_by_id_detail(phase_id):
  # try:
    phase = Phase.query.get(phase_id)
    if not phase:
      abort(404)

    return jsonify({
      'success': True,
      'phase': phase.serialize_with_tasks()
    })
  # except:
  #   print(sys.exc_info())
  #   abort(500)


@phase_bp.route('/phases', methods=['POST'])
@requires_auth('post:phases')
def create_phase(jwt_payload):
  body = request.get_json()
  if not body:
    abort(400)

  title = body.get('title')
  if not title:
    abort(422)
  
  if check_title_phase_exists(title):
    abort(409)

  try:
    phase = Phase(title=title)
    phase.insert()
    phase.commit()
  except:
    phase.rollback()
    print(sys.exc_info())
    abort(500)
  
  return jsonify({
    'success': True,
    'phase': phase.serialize()
  })


@phase_bp.route('/phases/<int:phase_id>', methods=['PATCH'])
@requires_auth('patch:phases')
def update_phase(jwt_payload, phase_id):
  body = request.get_json()
  if not body:
    abort(400)

  new_title = body.get('title')
  new_order = body.get('order')
  
  if not(new_title or new_order):
    abort(422)

  phase = Phase.query.get(phase_id)
  if not phase:
    abort(404)

  if check_title_phase_exists(new_title):
    abort(409)

  try:
    if new_title:
      phase.title = new_title

    prev_order = phase.order
    if new_order and new_order != prev_order:
      phase.order = new_order

      phases = reorder_phases(
        phase_id = phase.id, 
        prev_order = prev_order, 
        new_order = new_order
      )

      for phase_reordered in phases:
        phase.add_phase_to_session(phase_reordered)

    phase.commit()
  except:
    phase.rollback()
    print(sys.exc_info())
    abort(500)

  return jsonify({
    'success': True,
    'phase': phase.serialize()
  })


@phase_bp.route('/phases/<int:phase_id>', methods=['DELETE'])
@requires_auth('delete:phases')
def delete_phase(jwt_payload, phase_id):

  phase = Phase.query.get(phase_id)
  if not phase:
    abort(404)

  try:
    phase_id = phase.id
    prev_order = phase.order
    phase.delete()
    
    phases = reorder_phases(
      phase_id = phase_id, 
      prev_order = prev_order, 
      new_order = None
    )    

    for phase_reordered in phases:
      phase.add_phase_to_session(phase_reordered)

    phase.commit()
  except:
    phase.rollback()
    print(sys.exc_info())
    abort(500)

  return jsonify({
    'success': True,
    'phase_deleted': phase_id
  })


# @phase_bp.errorhandler(PhaseError)
# def handle_phase_error(error):
#   return jsonify({
#     'success': False,
#     'error': error.status_code,
#     'message': error.error['description']
#   }), error.status_code