import React, { createContext, useState, useContext } from 'react';
import axios from "axios";
import { AuthContext } from '../auth/AuthProvider';

export const TaskContext = createContext();

const BASE_URL = process.env.REACT_APP_API_URL;

const TaskProvider = ({ children }) => {
  const [tasks, setTasks] = useState([]);
  const { setToken } = useContext(AuthContext);

  const loadTasks = async () => {
    try {
      const config = await setToken();
      const res = await axios.get(`${BASE_URL}/tasks`, config);
      setTasks(res.data.tasks);
    } catch (err) {
      console.log(err);
    }
  }

  const addTask = async (task) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      const res = await axios.post(`${BASE_URL}/tasks`, task, config);
      setTasks([...tasks, res.data.task]);
    } catch (err) {
      console.log(err);
    }
  };

  const updateTask = async (task) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      const res = await axios.patch(`${BASE_URL}/tasks/${task.id}`, task, config);
      const tasksUpdated = res.data.tasks;
      setTasks(tasksUpdated);
    } catch (err) {
      console.log(err);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      const config = await setToken();
      config['headers']['Content-Type'] = 'application/json';

      await axios.delete(`${BASE_URL}/tasks/${taskId}`, config);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <TaskContext.Provider
      value={{
        tasks,
        loadTasks,
        addTask,
        updateTask,
        deleteTask
      }}
    >
      {children}
    </TaskContext.Provider>
  );

};

export default TaskProvider;