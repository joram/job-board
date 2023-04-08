import {Image} from "semantic-ui-react";

export default function Home(){
    let user = JSON.parse(sessionStorage.getItem("user"))
    let token = sessionStorage.getItem("token")
    console.log("user", user)
    return (
        <div>
            <Image src={user.profile_picture} avatar />
            <span>{user.name}</span>
        </div>
    )
}