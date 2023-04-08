import {Image} from "semantic-ui-react";
import {getLocalUser} from "../utils";
import {redirect} from "react-router-dom";
import {Configuration, PublicApi} from "./api_client/api.ts";

export default function Home(){
    let user = getLocalUser()
    if(user === null){
        redirect("/login")
    }
    let config = new Configuration({
        basePath: "https://ghrmz7xo12.execute-api.us-east-1.amazonaws.com/prod"
    })
    let api = new PublicApi(config)
    api.getCompaniesCompaniesGet().then((response) => {
      console.log(response)
    })
    return (
        <div>
            <Image src={user.profile_picture} avatar />
            <span>{user.name}</span>
        </div>
    )
}