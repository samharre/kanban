import React, { useState, useContext } from 'react';
import PropTypes from 'prop-types';
import { fade, makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import AddIcon from '@material-ui/icons/Add';
import ClearIcon from '@material-ui/icons/Clear';
import Fade from '@material-ui/core/Collapse';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import Button from '@material-ui/core/Button';
import { TaskContext } from '../providers/tasks/TaskProvider';

const useStyles = makeStyles((theme) => ({
  icon: {
    fontSize: 'large',
    padding: theme.spacing(0),
    marginBottom: theme.spacing(0.8),
    '&:hover': {
      borderRadius: '0',
      backgroundColor: fade('#000', 0),
      color: fade('#000', 0.8),
    }
  },
  addCard: {
    margin: theme.spacing(0.5, 1),
    backgroundColor: '#ebecf0',
    color: '#5e6c84',
    '&:hover': {
      backgroundColor: fade('#000', 0.1),
      cursor: 'pointer',
    }
  },
  addCardLabel: {
    display: 'inline',
    marginLeft: theme.spacing(0.5),
    padding: theme.spacing(0),
    fontSize: '0.95rem',
  },
  inputCard: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    marginTop: theme.spacing(0.5),
    marginLeft: theme.spacing(0.5)
  },
  addButton: {
    margin: theme.spacing(1),
    marginTop: theme.spacing(0.5),
    marginLeft: theme.spacing(0.5),
    padding: theme.spacing(0.8),
    fontWeight: 'bold'
  }
}));

const ListInput = ({ phaseId }) => {
  const classes = useStyles();
  const { addTask } = useContext(TaskContext);

  const [collapse, setCollapse] = useState(true);
  const [titleTask, setTitleTask] = useState('');

  const onChange = e => setTitleTask(e.target.value);

  const handleClickIcon = () => {
    setCollapse(!collapse)
    setTitleTask('');
  };

  const handleAddTask = () => {
    const title = titleTask;

    if (title) {
      addTask({
        title: title,
        phase_id: phaseId
      });
      setTitleTask('');
    }
  };

  return (
    <>
      <Fade in={collapse} timeout={0}>
        <Paper className={classes.addCard} elevation={0} onClick={handleClickIcon}>
          <IconButton className={classes.icon}>
            <AddIcon />
          </IconButton>
          <Typography className={classes.addCardLabel}>
            Add card
          </Typography>
        </Paper>
      </Fade>

      <Fade in={!collapse} timeout={0}>
        <Paper className={classes.inputCard}>
          <InputBase
            multiline
            fullWidth
            placeholder='Enter a title for this card...'
            rows={2}
            onChange={onChange}
            value={titleTask}
          />
        </Paper>
        <Button
          className={classes.addButton}
          variant="contained"
          color="primary"
          size='small'
          onClick={handleAddTask}
        >
          Add Card
        </Button>
        <IconButton className={classes.icon} onClick={handleClickIcon}>
          <ClearIcon />
        </IconButton>
      </Fade>
    </>
  );
};

ListInput.propTypes = {
  phaseId: PropTypes.number.isRequired
};

export default ListInput;
