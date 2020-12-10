import React, { useState } from "react";
import PropTypes from 'prop-types';
import { fade, makeStyles } from "@material-ui/core/styles";
import Popover from '@material-ui/core/Popover';
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from "@material-ui/icons/Delete";
import ClearIcon from "@material-ui/icons/Clear";
import Divider from "@material-ui/core/Divider";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme) => ({
  header: {
    margin: theme.spacing(2),
    fontSize: "0.9rem",
    flexGrow: "1",
    color: "#5e6c84",
  },
  icon: {
    padding: theme.spacing(1, 2, 1, 2),
    "&:hover": {
      borderRadius: "0",
      backgroundColor: fade("#000", 0),
      color: fade("#000", 0.8),
    }
  },
  deleteIcon: {
    padding: theme.spacing(0.5),
    marginBottom: theme.spacing(0.8),
    '&:hover': {
      borderRadius: '0',
      backgroundColor: fade('#000', 0),
      color: fade('#000', 0.8),
    }
  },
  content: {
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
  },
  divider: {
    width: "87%",
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    marginBottom: theme.spacing(1),
  },
  btn: {
    margin: theme.spacing(2),
    width: "87%",
    backgroundColor: "#cf513d",
    color: "#fff",
    "&:hover": {
      backgroundColor: fade("#cf513d", 0.8),
    }
  }
}));

const ModalDelete = ({ subject, handleDelete }) => {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleDeleteAction = () => {
    handleClose();
    handleDelete();
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>
      <IconButton className={classes.deleteIcon} onClick={handleClick} >
        <DeleteIcon fontSize='small' />
      </IconButton>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left"
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left"
        }}
      >
        <Box display="flex">
          <Typography className={classes.header}>{`Delete ${subject}`}</Typography>
          <IconButton className={classes.icon} onClick={handleClose}>
            <ClearIcon fontSize='small' />
          </IconButton>
        </Box>
        <Divider className={classes.divider} horizontal="center" />
        <Typography className={classes.content} variant='body2'>
          This action is irreversible.
      </Typography>
        <Typography className={classes.content} variant='body2'>
          Are you sure you want to delete?
      </Typography>
        <Button
          className={classes.btn}
          variant="contained"
          size="small"
          onClick={handleDeleteAction}
        >
          {`Delete ${subject}`}
        </Button>
      </Popover>
    </div>
  );
};

ModalDelete.propTypes = {
  subject: PropTypes.string.isRequired,
  handleDelete: PropTypes.func.isRequired
};

export default ModalDelete;