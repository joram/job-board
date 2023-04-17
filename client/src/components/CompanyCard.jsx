import {useNavigate} from "react-router";
import {Card, Image} from "semantic-ui-react";
import React from "react";
import {JobPostingPlaceholder} from "./JobPostingCard";
import {truncate} from "../utils";

export default function CompanyCard(props) {
    let {data} = props
    let navigate = useNavigate();
    if (data === undefined) {
        return <JobPostingPlaceholder/>
    }

    function redirect() {
        navigate("/company/"+data.id)
    }

    let jobCount = null
    if(data.num_jobs !== undefined){
        jobCount = <span> ({data.num_jobs})</span>
    }

    return <Card  onClick={() => redirect()}>
      <Card.Content>
        <Image
          floated='right'
          size='mini'
          src={data.logo_url}
        />
        <Card.Header>{data.name}{jobCount}</Card.Header>
        <Card.Description>{truncate(data.description, 300)}</Card.Description>
      </Card.Content>
    </Card>
}