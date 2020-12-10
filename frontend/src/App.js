import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Login from './pages/Login';
import ManagerPhase from './pages/ManagerPhase';
import { useAuth0 } from "@auth0/auth0-react";
import AuthProvider from './providers/auth/AuthProvider';
import history from './utils/history';
import PhaseProvider from './providers/phases/PhaseProvider';
import TaskProvider from './providers/tasks/TaskProvider';

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const { isAuthenticated } = useAuth0();

  return (
    <Route
      {...rest}
      render={props =>
        isAuthenticated ? (<Component {...props} />) :
          (<Login />)
      }
    />
  )
};

const App = () => {
  return (
    <>
      <Router history={history}>
        <AuthProvider>
          <Header />
          <PhaseProvider>
            <TaskProvider>
              <Switch>
                <ProtectedRoute exact path="/" component={Home} />
                <ProtectedRoute exact path="/phases" component={ManagerPhase} />
              </Switch>
            </TaskProvider>
          </PhaseProvider>
        </AuthProvider>
      </Router>
    </>
  );
};

export default App;
