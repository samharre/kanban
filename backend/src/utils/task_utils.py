from ..models.task import Task

def reorder_tasks_same_phase(phase_id, task_id, prev_order, new_order):
  tasks = []
  if not(phase_id and task_id):
    return tasks

  if not(prev_order or new_order):
    return tasks

  delta = 0
  query = Task.query.filter(Task.phase_id == phase_id)
  query = query.filter(Task.id != task_id)
  
  if not new_order:
    query = query.filter(Task.order >= prev_order)
    delta = -1
  elif prev_order > new_order:
    query = query.filter(Task.order >= new_order, Task.order <= prev_order)
    delta = 1
  elif prev_order < new_order:
    query = query.filter(Task.order >= prev_order, Task.order <= new_order)
    delta = -1
  else:
    return tasks

  query = query.order_by(Task.order)
  tasks = query.all()
  
  for task in tasks:
    task.order = task.order + delta
  
  return tasks


def reorder_tasks_diff_phases(prev_phase_id, new_phase_id, task_id, order_prev_phase, order_new_phase):
  tasks = []
  if not (prev_phase_id and new_phase_id and task_id and order_prev_phase and order_new_phase):
    return tasks

  if prev_phase_id == new_phase_id:
    return tasks

  query = Task.query.filter(Task.phase_id == prev_phase_id).\
    filter(Task.order >= order_prev_phase).\
    filter(Task.id != task_id).\
    order_by(Task.order)

  tasks_prev_phase = query.all()

  for task in tasks_prev_phase:
    task.order = task.order - 1
    tasks.append(task)  

  tasks_new_phase = Task.query.filter(Task.phase_id == new_phase_id).\
    filter(Task.order >= order_new_phase).\
    filter(Task.id != task_id).\
    order_by(Task.order).all()

  for task in tasks_new_phase:
    task.order = task.order + 1
    tasks.append(task)  

  return tasks