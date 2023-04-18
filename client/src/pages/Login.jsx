import React, {useEffect} from "react";
import {useNavigate} from "react-router";
import {useSearchParams} from "react-router-dom";
import {serverUrl} from "../utils";
import MainMenu from "../components/MainMenu";
import {Container} from "semantic-ui-react";

export default function Login() {
    let navigate = useNavigate();
    const [searchParams] = useSearchParams();
    let accessToken = searchParams.get("access_token")
    let name = searchParams.get("name")
    let profilePicture = searchParams.get("profile_picture")
    let id = searchParams.get("id")
    let isAdmin = searchParams.get("is_admin")
    let client_id = "44177235344-5s1uhr8fhj9c3hsrhb3pl5nh98evfk3n.apps.googleusercontent.com"
    let redirect_uri = serverUrl("/auth/google")


    useEffect(() => {
        if(accessToken === null || name === null || profilePicture === null){
            return
        }
        sessionStorage.setItem("user", JSON.stringify({
            accessToken: accessToken,
            name: name,
            profilePicture: profilePicture,
            isAdmin: isAdmin,
            id: id,
        })
        );
        navigate('/');
    })

  return <>
      <MainMenu highlight="Login"/>
    <Container textAlign="center">
        You should only need to create an account or login if you want to:
    </Container>
      <Container>
    <span>

        <ul>
            <li>create job postings</li>
            <li>create slack/email/sms notifications</li>
        </ul>

      <script src="https://accounts.google.com/gsi/client" async defer></script>
        <div id="g_id_onload"
             data-client_id={client_id}
             data-login_uri={redirect_uri}
             data-auto_prompt="false">
        </div>
        <div className="g_id_signin"
             data-type="standard"
             data-size="large"
             data-theme="outline"
             data-text="sign_in_with"
             data-shape="rectangular"
             data-logo_alignment="left"
        >
        </div>

    </span>

    </Container>

  </>
}