import {Container, Dropdown, Menu, Message} from "semantic-ui-react";
import React, {useState} from "react";
import {getLocalUser} from "../utils";
import {useNavigate} from "react-router";
import {Link} from "react-router-dom";


function ProfileMenu() {
    let user = getLocalUser()
    if(user === null){
        return <>
            <Menu.Item as={Link} to="/login" >Login</Menu.Item>
        </>
    }
    return <>
           <Dropdown item text={user.name}>
           <Dropdown.Menu>
             <Dropdown.Item as={Link} to="/my/companies" >My Companies</Dropdown.Item>
             <Dropdown.Item as={Link} to="/my/job_postings" >My Job Postings</Dropdown.Item>
             <Dropdown.Item as={Link} to="/logout" >Logout</Dropdown.Item>
           </Dropdown.Menu>
         </Dropdown>

    </>
}
export default function MainMenu(props) {
    let {highlight} = props
    let navigate = useNavigate();
    let [activeItem, setActiveItem] = useState(highlight)
    let handleItemClick = (e, { name, url }) => {
        setActiveItem(name)
        navigate(url)
    }

    return (<>

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
            <Container>
                <Message negative>
     <Message.Header>Under Active Development</Message.Header>
       We are actively developing this site. The data is test data, and the site is not yet ready for production use.
     </Message>
            </Container>
            <br/>
    </>
    )
}