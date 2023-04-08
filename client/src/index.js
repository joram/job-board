import React from "react";
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';

import {createBrowserRouter, RouterProvider,} from "react-router-dom";
import "./index.css";
import Login from "./pages/Login";
import SlackAuth from "./pages/SlackAuth";
import Home from "./pages/home";
import 'semantic-ui-css/semantic.min.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login/>,
  }, {
    path: "/home",
    element: <Home />,
  }, {
    path: "/api/v1/auth/slack",
    element: <SlackAuth />,
  },
]);



ReactDOM.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
reportWebVitals();