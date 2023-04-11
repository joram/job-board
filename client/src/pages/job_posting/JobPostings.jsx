import React, {useEffect} from 'react'
import JobPosting, {JobPostingPlaceholder} from "../../components/JobPostingCard";
import {useState} from "react";
import {get_all_companies, get_all_job_postings} from "../../api";
import {Card, Container} from "semantic-ui-react";
import MainMenu from "../../components/MainMenu";

export default function JobPostings(){
    let [loading, setLoading] = useState(true)
    let [jobPostings, setJobPostings] = useState([])

    useEffect(() => {
        get_all_job_postings().then(job_postings => {
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
    </>


}