import {useSearchParams} from "react-router-dom";
import {serverUrl} from "../utils";
import React, {useEffect} from "react";
import {Router, useNavigate} from "react-router";

export default function SlackAuth() {
    let navigate = useNavigate();
  const [searchParams] = useSearchParams();
  let code = searchParams.get("code")

    useEffect(() => {
        fetch(serverUrl("/login?" + new URLSearchParams({code: code})), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            params: {
                "code": code
            }
        }).then((response) =>  {
            if(response.status !== 200){
                console.log("failed")
                navigate('/auth/failure');
            }
            return response.json()
        }).then(response => {
            console.log("success", response)
            sessionStorage.setItem("user", JSON.stringify(response.user));
            sessionStorage.setItem("token", response.token);
            navigate('/home');
        })
    })
  return <>
    authenticating with server... {code}
  </>
}