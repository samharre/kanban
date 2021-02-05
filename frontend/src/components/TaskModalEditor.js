import React, { useState, useContext } from 'react';
import { makeStyles, fade } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import IconButton from "@material-ui/core/IconButton";
import ClearIcon from "@material-ui/icons/Clear";
import EditIcon from '@material-ui/icons/Edit';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { PhaseContext } from '../providers/phases/PhaseProvider';

const useStyles = makeStyles((theme) => ({
  field: {
    minWidth: 120,
    margin: theme.spacing(1),
  },
  btn: {
    margin: theme.spacing(2),
    padding: theme.spacing(1, 3, 1, 3)
  },
  editIcon: {
    padding: theme.spacing(0.5),
    marginBottom: theme.spacing(0.8),
    '&:hover': {
      borderRadius: '0',
      backgroundColor: fade('#000', 0),
      color: fade('#000', 0.8),
    }
  }
}));

const TaskModalEditor = ({ dialogTitle, taskToEdit, handleTaskAction }) => {
  const classes = useStyles();

  const taskInitialState = {
    phase_id: null,
    title: '',
    description: '',
    priority: '',
    due_date: null,
    order: '',
    user_id: ''
  }
  const [task, setTask] = useState(taskInitialState);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  let { phase_id, title, description, priority, due_date, order } = task;
  const { phases } = useContext(PhaseContext);

  const handleOpen = () => {
    if (taskToEdit) {
      setTask(taskToEdit);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setError(null);
  };

  const handleChange = (e) => {
    setTask({ ...task, [e.target.name]: e.target.value });
  };

  const submit = () => {
    if (!title) {
      setError('Phase title is required!');
      return;
    }
    handleClose();
    handleTaskAction(task);
    setTask(taskInitialState);
  };

  return (
    <>
      <IconButton className={classes.editIcon} onClick={handleOpen} >
        <EditIcon fontSize='small' />
      </IconButton>

      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title" fullWidth={true} maxWidth={"sm"}>
        <DialogTitle id="form-dialog-title">
          <Grid container spacing={3} justify="space-between">
            <Grid item xs={11}>
              <Typography variant='h5' align='center'>{dialogTitle}</Typography>
            </Grid>
            <Grid item xs>
              <IconButton onClick={handleClose} style={{ padding: '0' }}>
                <ClearIcon />
              </IconButton>
            </Grid>
          </Grid>
        </DialogTitle>

        <DialogContent>
          <Grid container justify="space-between">
            <TextField className={classes.field}
              label="Title"
              name="title"
              margin="dense"
              fullWidth
              value={title}
              required={true}
              error={!!error}
              helperText={error}
              onChange={handleChange}
            />

            <FormControl className={classes.field}>
              <InputLabel id="phase-label">Phase</InputLabel>
              <Select
                labelId="phase-label"
                id="phase"
                name="phase_id"
                value={phase_id}
                onChange={handleChange}
              >
                {phases.map((phase, index) => (
                  <MenuItem key={phase.id} value={phase.id}>{phase.title}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl className={classes.field}>
              <InputLabel id="task-priority-label">Priority</InputLabel>
              <Select
                labelId="task-priority-label"
                id="task-priority"
                name="priority"
                value={priority}
                onChange={handleChange}
              >
                <MenuItem value={'#ff0000'}>High</MenuItem>
                <MenuItem value={'#ffa500'}>Medium</MenuItem>
                <MenuItem value={'#56a274'}>Low</MenuItem>
              </Select>
            </FormControl>

            <TextField className={classes.field}
              id="date"
              label="Due date"
              type="date"
              name="due_date"
              value={due_date}
              InputLabelProps={{
                shrink: true,
              }}
              onChange={handleChange}
            />

            <FormControl className={classes.field}>
              <InputLabel id="task-order-label">Order</InputLabel>
              <Select
                labelId="task-order-label"
                id="task-order"
                name="order"
                value={order}
                onChange={handleChange}
              >
                <MenuItem value={1}>1</MenuItem>
                <MenuItem value={2}>2</MenuItem>
                <MenuItem value={3}>3</MenuItem>
              </Select>
            </FormControl>

            <TextField className={classes.field}
              id="outlined-multiline-static"
              margin="dense"
              label="Description"
              name="description"
              multiline
              rows={4}
              fullWidth
              value={description}
              onChange={handleChange}
            />
          </Grid>
        </DialogContent>

        <DialogActions>
          <Button className={classes.btn}
            color="primary"
            variant="contained"
            size="large"
            onClick={submit}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </>
  )
};

TaskModalEditor.defaultProps = {
  dialogTitle: 'Edit Task'
};

TaskModalEditor.propTypes = {
  dialogTitle: PropTypes.string.isRequired,
  handleTaskAction: PropTypes.func.isRequired,
  taskToEdit: PropTypes.object
};

export default TaskModalEditor;