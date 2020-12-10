import React, { createContext, useState, useContext } from 'react';
import axios from "axios";
import { AuthContext } from '../auth/AuthProvider';

export const PhaseContext = createContext();

const BASE_URL = process.env.REACT_APP_API_URL;

const PhaseProvider = ({ children }) => {
  const [phases, setPhases] = useState([]);
  const { setToken } = useContext(AuthContext);

  const loadPhases = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/phases`);
      setPhases(res.data.phases);
    } catch (err) {
      console.log(err);
    }
  };

  const addPhase = async (phase) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      const res = await axios.post(`${BASE_URL}/phases`, phase, config);
      setPhases([...phases, res.data.phase])

    } catch (err) {
      console.log(err);
    }
  };

  const updatePhase = async (phase) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      const res = await axios.patch(`${BASE_URL}/phases/${phase.id}`, phase, config);
      const phasesUpdated = res.data.phases;
      setPhases(phasesUpdated);
    } catch (err) {
      console.log(err);
    }
  };

  const deletePhase = async (phaseId) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      await axios.delete(`${BASE_URL}/phases/${phaseId}`, config);
      setPhases(phases.filter(phase => phase.id !== phaseId));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <PhaseContext.Provider
      value={{
        phases,
        loadPhases,
        addPhase,
        updatePhase,
        deletePhase
      }}
    >
      {children}
    </PhaseContext.Provider>
  );

};

export default PhaseProvider;