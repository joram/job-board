import {Dropdown, Menu} from "semantic-ui-react";
import React, {useState} from "react";
import {clientUrl, getLocalUser} from "../utils";
import SlackLogin from "./SlackLogin";
import {useNavigate} from "react-router";
import {Link} from "react-router-dom";

function ProfileMenu() {
    let user = getLocalUser()
    if(user == null){
        return <SlackLogin
        redirectUrl={clientUrl('/api/v1/auth/slack')}
        slackClientId='735117853430.5091553447984'
        slackUserScope='openid profile'
      />
    }

    return <Dropdown item text={user.name}>
          <Dropdown.Menu>
            <Dropdown.Item as={Link} to="/my/companies" >My Companies</Dropdown.Item>
            <Dropdown.Item as={Link} to="/my/job_postings" >My Job Postings</Dropdown.Item>
            <Dropdown.Item as={Link} to="/logout" >Logout</Dropdown.Item>
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