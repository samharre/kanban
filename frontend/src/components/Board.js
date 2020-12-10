import React, { useContext, useEffect } from 'react';
import Box from '@material-ui/core/Box';
import List from '../components/List';
import { PhaseContext } from '../providers/phases/PhaseProvider';
import { TaskContext } from '../providers/tasks/TaskProvider';

const Board = () => {
  const { phases, loadPhases } = useContext(PhaseContext);
  const { tasks, loadTasks } = useContext(TaskContext);

  useEffect(() => {
    loadPhases();
    loadTasks();
  }, []);

  return (
    <>
      {phases && tasks && <Box display="flex" flexWrap="wrap" ml={1}>
        {phases.map(phase =>
          <List
            key={phase.id}
            phase={phase}
            tasks={tasks.filter(task => task.phase_id === phase.id)}
          />)}
      </Box>}
    </>
  );
};

export default Board;
