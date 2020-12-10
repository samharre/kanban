import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import LateralMenu from '../components/LateralMenu';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import { useAuth0 } from "@auth0/auth0-react";

const useStyles = makeStyles((theme) => ({
  avatar: {
    width: theme.spacing(5),
    height: theme.spacing(5),
  },
  toolbarTitle: {
    flexGrow: 1,
    paddingLeft: theme.spacing(1),
    fontSize: '1.3rem',
    fontWeight: 'bold',
  },
}));

const Header = () => {
  const classes = useStyles();

  const {
    user,
    isAuthenticated,
    loginWithRedirect,
    logout,
  } = useAuth0();

  return (
    <>
      <AppBar position="static" >
        <Toolbar>
          <LateralMenu />
          <Typography className={classes.toolbarTitle}>
            Kanban
          </Typography>
          {isAuthenticated && (
            <>
              <Button
                color="inherit"
                onClick={() => {
                  localStorage.removeItem('token');
                  localStorage.removeItem('userId');
                  logout({
                    returnTo: window.location.origin,
                  })
                }}
              >
                Logout
              </Button>
              <Avatar
                className={classes.avatar}
                alt="User"
                src={user.picture}
              />
            </>
          )}
          {!isAuthenticated && (
            <Button
              color="inherit"
              onClick={() => {
                return loginWithRedirect()
              }}
            >
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>
    </>
  );
};

export default Header;
