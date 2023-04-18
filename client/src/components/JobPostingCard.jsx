import React from 'react'
import {Card, Image, Placeholder} from 'semantic-ui-react'
import {useNavigate} from "react-router";



export function JobPostingPlaceholder(){
  return <Placeholder>
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
  </Placeholder>
}

export default function JobPostingCard(props){
    let {data} = props
    let navigate = useNavigate();
    if (data === undefined) {
        return <JobPostingPlaceholder/>
    }

    function redirect() {
        let details_url="/job_posting/"+data.id
        navigate(details_url)
    }


    return <Card  onClick={() => redirect()}>
      <Card.Content>
          {data.company === null ? null : <Image
              floated='right'
              size='mini'
              src={data.company.logo_url}
            />
        }
        <Card.Header>{data.job_title}</Card.Header>
        <Card.Meta>{data.company === null ? null : data.company.name}</Card.Meta>
        <Card.Description>{data.description}</Card.Description>
      </Card.Content>
      <Card.Content extra>
        {data.min_salary} - {data.max_salary} {data.salary_currency}
      </Card.Content>
    </Card>
}
