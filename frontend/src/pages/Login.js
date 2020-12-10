import React from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import Button from '@material-ui/core/Button';
import '../App.css';

const Login = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="centered">
      <h1>Kanban</h1>
      <p>
        An application inspired on <a href="https://trello.com">Trello</a> to help managing any project end-to-end.
      </p>
      <Button style={{ margin: '10px' }}
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