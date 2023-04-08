import {Image} from "semantic-ui-react";
import {getLocalUser} from "../utils";
import {redirect} from "react-router-dom";

export default function Home(){
    let user = getLocalUser()
    if(user === null){
        redirect("/login")
    }

    return (
        <div>
            <Image src={user.profile_picture} avatar />
            <span>{user.name}</span>
        </div>
    )
}