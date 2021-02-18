import React, { useState, useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Fab from '@material-ui/core/Fab';
import IconButton from "@material-ui/core/IconButton";
import ClearIcon from "@material-ui/icons/Clear";
import AddIcon from '@material-ui/icons/Add';
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
  }
}));

const PhaseModalEditor = ({ dialogTitle, phaseToEdit, handlePhaseAction }) => {
  const [open, setOpen] = useState(false);
  const classes = useStyles();

  const phaseInitialState = {
    title: '',
    order: '',
    can_create_task: ''
  }
  const editPhase = phaseToEdit;

  const [phase, setPhase] = useState(phaseInitialState);
  const [error, setError] = useState(null);
  let { title, order, can_create_task } = phase;
  const { phases } = useContext(PhaseContext);

  const handleOpen = () => {
    if (phaseToEdit) {
      setPhase(phaseToEdit);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setError(null);
  };

  const handleChange = (e) => {
    setPhase({ ...phase, [e.target.name]: e.target.value });
  };

  const submit = () => {
    if (!title) {
      setError('Phase title is required!');
      return;
    }
    handleClose();
    handlePhaseAction(phase);
    setPhase(phaseInitialState);
  };
  return (
    <>
      {editPhase &&
        <IconButton onClick={handleOpen} >
          <EditIcon fontSize='small' />
        </IconButton>
      }
      {!editPhase &&
        <Fab
          color="primary"
          aria-label="add"
          size="small"
          onClick={handleOpen}
        >
          <AddIcon />
        </Fab>
      }

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
            <TextField className={classes.field} autoComplete="off"
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

            {editPhase &&
              <FormControl className={classes.field}>
                <InputLabel id="phase-order-label">Order</InputLabel>
                <Select
                  labelId="phase-order-label"
                  id="phase-order"
                  name="order"
                  value={order}
                  onChange={handleChange}
                >
                  {phases.map((phase, index) => (
                    <MenuItem key={phase.id} value={index + 1}>{index + 1}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            }
            
            <FormControl className={classes.field} style={{ width: '200px' }}>
              <InputLabel id="phase-create-task-label">Can Create Task</InputLabel>
              <Select
                labelId="phase-create-task-label"
                id="phase-create-task"
                name="can_create_task"
                value={!!can_create_task ? can_create_task : false}
                onChange={handleChange}
              >
                <MenuItem value={true}>Yes</MenuItem>
                <MenuItem value={false}>No</MenuItem>
              </Select>
            </FormControl>
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

PhaseModalEditor.defaultProps = {
  dialogTitle: 'Add Phase'
};

PhaseModalEditor.propTypes = {
  dialogTitle: PropTypes.string.isRequired,
  handlePhaseAction: PropTypes.func.isRequired,
  phaseToEdit: PropTypes.object
};

export default PhaseModalEditor;