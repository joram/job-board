import React, {useEffect, useState} from 'react'
import {JobPostingPlaceholder} from "../components/JobPostingCard";
import {delete_company, get_company_by_id, get_user_id} from "../api";
import {Modal, Header, Segment, Button, Container, Image} from "semantic-ui-react";
import MainMenu from "../components/MainMenu";
import {useParams} from 'react-router-dom';
import {Link} from "react-router-dom";
import {useNavigate} from "react-router";

export default function Company(){
    let [loading, setLoading] = useState(true)
    let [company, setCompany] = useState([])
    let [deleteModalOpen, setDeleteModalOpen] = useState(false)
    let { company_id } = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        get_company_by_id(company_id).then(got_company => {
            setCompany(got_company)
            setLoading(false)
        })
    }, [])

    if(loading) {
        return <Container>
            <h1>Company Details</h1>
            <JobPostingPlaceholder/>
            <JobPostingPlaceholder/>
        </Container>
    }

    if(company.name === ""){
        company.name = "Unknown Company"
    }
    if(company.description === ""){
        company.description = "No description available"
    }
    let logoImg = null;
    if(company.logo_url !== ""){
        logoImg = <Image src={company.logo_url} alt="Company Logo" size="small" />
    }
    let adminMenu = null;


    if(company.user_id === get_user_id()){
        adminMenu = <Segment>
            <Button as={Link} to={"/company/"+company.id+"/edit"}>Edit</Button>
            <Button onClick={() => setDeleteModalOpen(true)}>Delete</Button>
        </Segment>
    }
    return <>
        <MainMenu highlight={"Companies"}/>
        <Container>
           {adminMenu}
            <h1>{company.name}</h1>
            <Segment>{company.description}</Segment>
            {logoImg}
        </Container>

        <Modal
          onClose={() => setDeleteModalOpen(false)}
          onOpen={() => setDeleteModalOpen(true)}
          open={deleteModalOpen}
        >
          <Modal.Header>Delete Company?</Modal.Header>
          <Modal.Content image>
            <Image size='medium' src={company.logo_url} wrapped />
            <Modal.Description>
              <Header>{company.name} </Header>
              <p>
                Are you sure you want to delete the company and all of it's attached job postings?
              </p>
            </Modal.Description>
          </Modal.Content>
          <Modal.Actions>
            <Button color='black' onClick={() => setDeleteModalOpen(false)}>
              Cancel
            </Button>
            <Button
              content="Delete"
              onClick={() => {
                  setDeleteModalOpen(false)
                    delete_company(company.id).then(r => {
                        navigate("/my/companies")
                    })
              }}
              negative
            />
          </Modal.Actions>
        </Modal>
    </>


}