import React from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import Button from '@material-ui/core/Button';
import '../App.css';

const Login = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="centered">
      <h1 style={{fontSize: '2.7rem'}}>Kanban</h1>
      <p style={{fontSize: '1.2rem'}}>
        An application inspired on <a href="https://trello.com">Trello</a> to help managing projects.
      </p>
      <Button style={{ margin: '15px' }}
        color="primary"
        variant="contained"
        size="large"
        onClick={() => {
          return loginWithRedirect()
        }}
      >
        Login
      </Button>
    </div>
  );
};

export default Login;