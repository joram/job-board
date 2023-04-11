import React, {useEffect} from 'react'
import JobPosting, {JobPostingPlaceholder} from "../components/JobPostingCard";
import {useState} from "react";
import {get_all_companies, get_all_job_postings} from "../api";
import {Card, Container} from "semantic-ui-react";
import CompanyCard from "../components/CompanyCard";
import MainMenu from "../components/MainMenu";

export default function Companies(){
    let [loading, setLoading] = useState(true)
    let [companies, setCompanies] = useState([])

    useEffect(() => {
        get_all_companies().then(got_companies => {
            setCompanies(got_companies)
            setLoading(false)
        })
    }, [])

    if(loading) {
        return <Container>
            <h1>Job Postings</h1>
            <JobPostingPlaceholder/>
            <JobPostingPlaceholder/>
        </Container>
    }

    let i = 0;
    return <>
        <MainMenu highlight={"Companies"}/>
        <Container>
            <Card.Group itemsPerRow={3}>
                {companies.map(company => {
                    return <CompanyCard key={"company_"+i++} data={company} />
                })}
            </Card.Group>
        </Container>
        </>


}