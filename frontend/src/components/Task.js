import React, { useState, useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Box from '@material-ui/core/Box';
import Paper from '@material-ui/core/Paper';
import { Typography } from '@material-ui/core';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import ModalDelete from './ModalDelete';
import TaskModalEditor from './TaskModalEditor';
import { TaskContext } from '../providers/tasks/TaskProvider';

const useStyles = makeStyles((theme) => ({
  task: {
    margin: theme.spacing(0.5),
    marginBottom: theme.spacing(1),
    padding: theme.spacing(1)
  },
  icon: {
    padding: theme.spacing(0)
  },
  label: {
    width: '30px',
    height: '8px',
    borderRadius: '5px'
  },
  timeIcon: {
    width: '12px',
    height: '25px',
    marginRight: theme.spacing(0.5)
  },
  date: {
    width: '50px',
    height: '15px',
  }
}));

const Task = ({ task }) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const { updateTask, deleteTask } = useContext(TaskContext);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleDeleteTask = () => {
    deleteTask(task.id);
  };

  const handleEditTask = (task) => {
    updateTask(task);
  };

  return (
    <>
      <Paper className={classes.task} >
        <>
          <Box display='flex' justifyContent='space-between'>
            {task.priority &&
              <Box m={0.5} bgcolor={task.priority} className={classes.label} />
            }
            {task.due_date &&
              <Typography component='div'>
                <Box mr={0.5} fontSize={11} display='flex' justifyContent="space-around">
                  <AccessTimeIcon fontSize='small' className={classes.timeIcon} />
                  <Box mt={0.7}>{task.due_date.toString().substr(5, 11)}</Box>
                </Box>
              </Typography>
            }
          </Box>
          <Box display='flex'>
            <Box flexGrow={1} onClick={handleOpen} p={0.5}>
              {task.title}
            </Box>
            <Box>
              <TaskModalEditor taskToEdit={task} handleTaskAction={handleEditTask} />
            </Box>
            <Box>
              <ModalDelete subject={'Task'} handleDelete={handleDeleteTask} />
            </Box>
          </Box>
        </>
      </Paper>
    </>
  )
};

Task.propTypes = {
  task: PropTypes.object.isRequired,
};

export default Task;
