import React, {useEffect} from "react";
import {useNavigate} from "react-router";

export default function Logout() {
    let navigate = useNavigate();

    useEffect(() => {
        sessionStorage.removeItem("user");
        navigate('/');
    })
  return <>
    logging out...
  </>
}