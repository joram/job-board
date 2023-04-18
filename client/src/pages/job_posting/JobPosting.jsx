import React, {useEffect, useState} from 'react'
import {JobPostingPlaceholder} from "../../components/JobPostingCard";
import {delete_job_posting, get_job_posting, get_user_id} from "../../api";
import {Button, Container, Header, Image, Modal, Segment, Table} from "semantic-ui-react";
import MainMenu from "../../components/MainMenu";
import {Link, useParams} from 'react-router-dom';
import {useNavigate} from "react-router";
import {getLocalUser} from "../../utils";

export default function JobPosting(){
    let [loading, setLoading] = useState(true)
    let [jobPosting, setJobPosting] = useState(null)
    let [deleteModalOpen, setDeleteModalOpen] = useState(false)
    let { job_posting_id } = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        get_job_posting(job_posting_id).then(job_posting => {
            setJobPosting(job_posting)
            setLoading(false)
        })
    }, [])

    if(loading) {
        return <>
            <MainMenu highlight={'Job Postings'}/>
            <Container>
                <JobPostingPlaceholder/>
                <JobPostingPlaceholder/>
            </Container>
        </>
    }

    let adminMenu = null;
    if(jobPosting.user_id === get_user_id() || getLocalUser().isAdmin ){
        adminMenu = <span>
            <Button as={Link} to={"/job_posting/"+jobPosting.id+"/edit"}>Edit</Button>
            <Button onClick={() => setDeleteModalOpen(true)}>Delete</Button>
        </span>
    }

    return <>
        <MainMenu highlight={'Job Postings'}/>
        <Container>
            <Table basic>
                <Table.Body>
                <Table.Row>
                    <Table.Cell>
                        <h1>{jobPosting.job_title} {adminMenu}</h1>
                        <h3><Link to={"/company/"+jobPosting.company.id}>{jobPosting.company.name}</Link></h3>
                        <h4>{jobPosting.min_salary}-{jobPosting.max_salary} {jobPosting.salary_currency}</h4>
                    </Table.Cell>
                    <Table.Cell>
                        <Segment basic align='right'>
                        <Image src={jobPosting.company.logo_url} size='small' />
                        </Segment>
                    </Table.Cell>
                </Table.Row>
                </Table.Body>
            </Table>

            <Segment.Group>
                <Segment>
                    <h3>Job Description</h3>
                    {jobPosting.description}
                </Segment>
                <Segment>
                    <h3>Requirements</h3>
                    {jobPosting.requirements}
                </Segment>
                <Segment>
                    <h3>Benefits</h3>
                    {jobPosting.benefits}
                </Segment>
            </Segment.Group>
            <Button as={Link} to={jobPosting.application_url}>Apply</Button>
        </Container>
        <Modal
          onClose={() => setDeleteModalOpen(false)}
          onOpen={() => setDeleteModalOpen(true)}
          open={deleteModalOpen}
        >
          <Modal.Header>Delete Job Posting?</Modal.Header>
          <Modal.Content image>
            <Modal.Description>
              <Header>{jobPosting.job_title} </Header>
              <p>
                Are you sure you want to delete this job posting?
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
                    delete_job_posting(jobPosting.id).then(r => {
                        navigate("/my/job_postings")
                    })
              }}
              negative
            />
          </Modal.Actions>
        </Modal>
    </>


}