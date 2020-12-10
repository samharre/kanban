import React, { createContext, useState, useEffect } from 'react';
import jwt_decode from "jwt-decode";
import { useAuth0 } from "@auth0/auth0-react";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [permissions, setPermissions] = useState([]);
  const { isAuthenticated, getAccessTokenSilently } = useAuth0()

  useEffect(() => {
    const getUserPermissions = async () => {
      if (isAuthenticated) {
        const jwt = await getAccessTokenSilently();
        console.log('Token JWT: ', jwt);

        if (jwt) {
          const jwt_decoded = jwt_decode(jwt);
          if (jwt_decoded.permissions) {
            setPermissions(jwt_decoded.permissions);
          }
        }
      }
    };
    getUserPermissions();

  }, [getAccessTokenSilently]);

  const setToken = async () => {
    const token = await getAccessTokenSilently();
    const config = {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    };
    return config;
  };

  const checkPermission = (permission) => {
    return permissions && permissions.length && permissions.indexOf(permission) >= 0;
  }

  return (
    <AuthContext.Provider
      value={{
        permissions,
        setToken,
        checkPermission
      }}
    >
      {children}
    </AuthContext.Provider>
  );

};

export default AuthProvider;