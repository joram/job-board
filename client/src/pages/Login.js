import '../App.css';
import SlackLogin from '../components/SlackLogin';
import React from "react";

function Login() {
  return (
    <div className="App">
        <br/>
      <SlackLogin
        redirectUrl='https://localhost:3000/api/v1/auth/slack'
        slackClientId='735117853430.5091553447984'
        slackUserScope='openid profile'
      />
    </div>
  );
}
export default Login;
