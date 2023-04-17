import React from "react";
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';

import {createBrowserRouter, RouterProvider,} from "react-router-dom";
import "./index.css";
import SlackAuth from "./pages/SlackAuth";
import 'semantic-ui-css/semantic.min.css'
import Companies from "./pages/company/Companies";
import JobPostings from "./pages/job_posting/JobPostings";
import Logout from "./pages/Logout";
import Login from "./pages/Login";
import MyCompanies from "./pages/company/MyCompanies";
import CreateCompany from "./pages/company/CreateCompany";
import Company from "./pages/company/Company";
import EditCompany from "./pages/company/EditCompany";
import MyJobPostings from "./pages/job_posting/MyJobPostings";
import CreateJobPosting from "./pages/job_posting/CreateJobPosting";
import {GoogleOAuthProvider} from '@react-oauth/google';


const router = createBrowserRouter([
  {
    path: "/",
    element: <JobPostings />,
  }, {
    path: "/companies",
    element: <Companies />,
  }, {
    path: "/company/:company_id",
    element: <Company/>,
  }, {
    path: "/company/:company_id/edit",
    element: <EditCompany />,
  }, {
    path: "/my/companies",
    element: <MyCompanies />,
  }, {
    path: "/my/job_postings",
    element: <MyJobPostings/>,
  }, {
    path: "/job_posting/create",
    element: <CreateJobPosting />,
  }, {
    path: "/company/create",
    element: <CreateCompany />,
  }, {
    path: "/api/v1/auth/slack",
    element: <SlackAuth />,
  }, {
    path: "/login",
    element: <Login />,
  }, {
    path: "/logout",
    element: <Logout />,
  }

]);



ReactDOM.render(
        <GoogleOAuthProvider clientId="44177235344-5s1uhr8fhj9c3hsrhb3pl5nh98evfk3n.apps.googleusercontent.com">
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
    </GoogleOAuthProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
reportWebVitals();