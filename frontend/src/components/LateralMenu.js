import React, { useState, useContext } from 'react';
import { AuthContext } from '../providers/auth/AuthProvider';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import SwipeableDrawer from '@material-ui/core/SwipeableDrawer';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import HomeIcon from '@material-ui/icons/Home';
import ViewColumnIcon from '@material-ui/icons/ViewColumn';

const useStyles = makeStyles(() => ({
  list: {
    width: 200
  },
  link: {
    textDecoration: 'none',
    '&:visited': {
      color: 'inherit'
    }
  }
}));

const LateralMenu = () => {
  const classes = useStyles();
  const [menu, setMenu] = useState(false);
  const { checkPermission } = useContext(AuthContext);

  const toggleDrawer = (open) => (event) => {
    if (event && event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setMenu(open);
  };

  const list = () => (
    <div
      className={classes.list}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        <ListItem button>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <Link to='/' className={classes.link}>My Board</Link>
        </ListItem>
        {
          !!checkPermission('post:phases') &&
          <ListItem button>
            <ListItemIcon>
              <ViewColumnIcon />
            </ListItemIcon>
            <Link to='/phases' className={classes.link}>Phases</Link>
          </ListItem>
        }
      </List>
    </div>
  );

  return (
    <div>
      <IconButton
        edge="start"
        color="inherit"
        aria-label="menu"
        onClick={toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>
      <SwipeableDrawer
        open={menu}
        onClose={toggleDrawer(false)}
        onOpen={toggleDrawer(true)}
      >
        {list()}
      </SwipeableDrawer>
    </div>
  );
};

export default LateralMenu;