import React from "react";
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';

import {createBrowserRouter, RouterProvider,} from "react-router-dom";
import "./index.css";
import SlackAuth from "./pages/SlackAuth";
import 'semantic-ui-css/semantic.min.css'
import Companies from "./pages/Companies";
import JobPostings from "./pages/JobPostings";

const router = createBrowserRouter([
  {
    path: "/",
    element: <JobPostings />,
  }, {
    path: "/companies",
    element: <Companies />,
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