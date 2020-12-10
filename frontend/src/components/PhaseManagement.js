import React, { useContext, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import ModalDelete from './ModalDelete';
import PhaseModalEditor from './PhaseModalEditor';
import { PhaseContext } from '../providers/phases/PhaseProvider';

const useStyles = makeStyles((theme) => ({
  table: {
    width: 'auto',
    border: 'none',
    margin: theme.spacing(5)
  },
  tableTitle: {
    fontWeight: 'bold'
  }
}));

const PhaseManagement = () => {
  const classes = useStyles();
  const { phases, loadPhases, addPhase, updatePhase, deletePhase } = useContext(PhaseContext);

  useEffect(() => {
    loadPhases();
  }, []);

  const handleAddPhase = (phase) => {
    addPhase(phase);
  };

  const handleEditPhase = (phase) => {
    updatePhase(phase);
  };

  const handleDeletePhase = (phaseId) => {
    deletePhase(phaseId);
  };

  return (
    <TableContainer className={classes.table} >
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className={classes.tableTitle}>Title</TableCell>
            <TableCell className={classes.tableTitle} align="right">Order</TableCell>
            <TableCell className={classes.tableTitle} align="right">Can Create Task</TableCell>
            <TableCell align="right">&nbsp;</TableCell>
            <TableCell align="right"><PhaseModalEditor handlePhaseAction={handleAddPhase} /></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {phases.map((phase) => (
            <TableRow key={phase.id}>
              <TableCell component="th" scope="row">
                {phase.title}
              </TableCell>
              <TableCell align="right">{phase.order}</TableCell>
              <TableCell align="right">{phase.can_create_task ? 'Yes' : 'No'}</TableCell>
              <TableCell align="right" size="small">
                {<PhaseModalEditor handlePhaseAction={handleEditPhase} phaseToEdit={phase} dialogTitle={'Edit Phase'} />}
              </TableCell>
              <TableCell align="right" size="small">
                {<ModalDelete subject={'Phase'} handleDelete={() => handleDeletePhase(phase.id)} />}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PhaseManagement;
