from ..models.phase import Phase

def reorder_phases(phase_id, prev_order, new_order):
  phases = []

  query = Phase.query.filter(Phase.id != phase_id)
  delta = 0
  if not new_order:
    query = query.filter(Phase.order >= prev_order)
    delta = -1

  elif prev_order > new_order:
    query = query.filter(Phase.order >= new_order, Phase.order <= prev_order)
    delta = 1

  elif prev_order < new_order:
    query = query.filter(Phase.order >= prev_order, Phase.order <= new_order)
    delta = -1

  query = query.order_by(Phase.order)
  phases = query.all()
  for phase in phases:
    phase.order = phase.order + delta
        
  return phases


def check_title_phase_exists(title):
  phase = Phase.query.filter(Phase.title == title).all()

  return len(phase) > 0