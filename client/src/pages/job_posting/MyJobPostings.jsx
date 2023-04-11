import React, {useEffect, useState} from 'react'
import JobPosting, {JobPostingPlaceholder} from "../../components/JobPostingCard";
import {get_my_job_postings} from "../../api";
import {Divider, Button, Card, Container} from "semantic-ui-react";
import MainMenu from "../../components/MainMenu";
import {Link} from "react-router-dom";

export default function MyJobPostings(){
    let [loading, setLoading] = useState(true)
    let [jobPostings, setJobPostings] = useState([])

    useEffect(() => {
        get_my_job_postings().then(job_postings => {
            setJobPostings(job_postings)
            setLoading(false)
        })
    }, [])

    if(loading) {
        return <Container>
            <JobPostingPlaceholder/>
            <JobPostingPlaceholder/>
        </Container>
    }

    let i = 0;
    return <>
        <MainMenu highlight={'Job Postings'}/>
        <Container>
            <Card.Group itemsPerRow={3}>
                {jobPostings.map(job_posting => {
                    return <JobPosting key={"posting_"+i++} data={job_posting} />
                })}
            </Card.Group>
        </Container>
        <Divider/>
        <Container textAlign="center">
            <Button as={Link} to="/job_posting/create" positive>Create</Button>
        </Container>
    </>


}