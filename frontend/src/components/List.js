import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import Task from './Task';
import ListInput from './ListInput';
import { AuthContext } from '../providers/auth/AuthProvider';

const useStyles = makeStyles((theme) => ({
  list: {
    width: '260px',
    marginTop: theme.spacing(1.5),
    margin: theme.spacing(0.5),
    padding: theme.spacing(0.5),
    backgroundColor: '#ebecf0',
    minHeight: '10vh'
  },
  listTitle: {
    padding: theme.spacing(1),
    marginBottom: theme.spacing(1),
    fontWeight: 'bold',
    fontSize: '0.9rem',
  },
  listContent: {
    width: '255px',
    paddingRight: theme.spacing(1),
    maxHeight: '70vh',
    overflow: 'auto'
  },
}));

const List = ({ phase, tasks }) => {
  const classes = useStyles();
  const { checkPermission } = useContext(AuthContext);

  return (
    <div>
      <Paper className={classes.list}>
        <Typography className={classes.listTitle}>
          {phase.title}
        </Typography>

        <Box className={classes.listContent}>
          {tasks.map(task =>
            <Task key={task.id} task={task} />)}
        </Box>

        {phase.can_create_task && !!checkPermission('post:tasks') && <ListInput phaseId={phase.id} />}
      </Paper>
    </div>
  )
};

List.propTypes = {
  phase: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired
};

export default List;
