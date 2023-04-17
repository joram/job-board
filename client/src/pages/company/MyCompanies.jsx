import React, {useEffect, useState} from 'react'
import {JobPostingPlaceholder} from "../../components/JobPostingCard";
import {get_my_companies} from "../../api";
import {Button, Card, Container, Divider} from "semantic-ui-react";
import CompanyCard from "../../components/CompanyCard";
import MainMenu from "../../components/MainMenu";
import {Link} from "react-router-dom";

export default function MyCompanies(){
    let [loading, setLoading] = useState(true)
    let [companies, setCompanies] = useState([])
    const [width, setWidth] = useState(window.innerWidth);
    const isMobile = width <= 768;

    function handleWindowSizeChange() {
        setWidth(window.innerWidth);
    }
    useEffect(() => {
        window.addEventListener('resize', handleWindowSizeChange);
        return () => {
            window.removeEventListener('resize', handleWindowSizeChange);
        }
    }, []);


    useEffect(() => {
        get_my_companies().then(got_companies => {
            setCompanies(got_companies)
            setLoading(false)
        })
    }, [])

    if(loading) {
        return <Container>
            <MainMenu highlight={"Companies"}/>
            <h1>My Companies</h1>
            <JobPostingPlaceholder/>
            <JobPostingPlaceholder/>
        </Container>
    }

    let itemsPerRow = 3
    if(isMobile){
        itemsPerRow = 1
    }
    let i = 0;
    return <>
        <MainMenu highlight={"Companies"}/>
        <Container>
            <Card.Group itemsPerRow={itemsPerRow} centered>
                {companies.map(company => {
                    return <CompanyCard key={"company_"+i++} data={company} />
                })}
            </Card.Group>
        </Container>
            <Container textAlign="center">
                <Button as={Link} to="/company/create" positive>Create</Button>
            </Container>
        </>


}