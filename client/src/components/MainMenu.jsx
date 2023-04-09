import {Dropdown, Image, Menu} from "semantic-ui-react";
import React, {useState} from "react";
import {getLocalUser} from "../utils";
import SlackLogin from "./SlackLogin";
import {useNavigate} from "react-router";

function ProfileMenu() {
    let user = getLocalUser()
    if(user == null){
        return <SlackLogin
        redirectUrl='https://localhost:3000/api/v1/auth/slack'
        slackClientId='735117853430.5091553447984'
        slackUserScope='openid profile'
      />
    }

    let profile = <>
        <Image src={user.profile_picture} avatar />
        <span>{user.name}</span>
    </>
    return <Dropdown item text={profile}>
          <Dropdown.Menu>
            <Dropdown.Item>My Companies</Dropdown.Item>
            <Dropdown.Item>My Job Postings</Dropdown.Item>
            <Dropdown.Item>Logout</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
}
export default function MainMenu(props) {
    let {highlight} = props
    let navigate = useNavigate();
    let [activeItem, setActiveItem] = useState(highlight)
    let handleItemClick = (e, { name, url }) => {
        setActiveItem(name)
        navigate(url)
    }

    return (
     <Menu pointing secondary>
       <Menu.Header><h1>Job Board</h1></Menu.Header>
       <Menu.Item
         name='Job Postings'
         url='/'
         active={activeItem === 'Job Postings'}
         onClick={handleItemClick}
       />
       <Menu.Item
         name='Companies'
         url='/companies'
         active={activeItem === 'Companies'}
         onClick={handleItemClick}
       />
       <Menu.Item position='right'>
         <ProfileMenu/>
       </Menu.Item>
     </Menu>
    )
}