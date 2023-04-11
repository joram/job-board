import {useNavigate} from "react-router";
import {Card, Image} from "semantic-ui-react";
import React from "react";
import {JobPostingPlaceholder} from "./JobPostingCard";

export default function CompanyCard(props) {
    let {data} = props
    let navigate = useNavigate();
    if (data === undefined) {
        return <JobPostingPlaceholder/>
    }

    function redirect() {
        navigate("/company/"+data.id)
    }

    console.log(data)
    return <Card  onClick={() => redirect()}>
      <Card.Content>
        <Image
          floated='right'
          size='mini'
          src={data.logo_url}
        />
        <Card.Header>{data.name}</Card.Header>
        <Card.Description>{data.description}</Card.Description>
      </Card.Content>
    </Card>
}