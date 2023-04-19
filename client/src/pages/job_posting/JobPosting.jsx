import React, {useEffect, useState} from 'react'
import {JobPostingPlaceholder} from "../../components/JobPostingCard";
import {delete_job_posting, get_job_posting, get_user_id} from "../../api";
import {Button, Container, Header, Item, Modal, Label} from "semantic-ui-react";
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
    }, [job_posting_id])

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
    if(jobPosting.user_id === get_user_id() || (getLocalUser() !== null && getLocalUser().isAdmin) ){
        adminMenu = <span>
            <Button as={Link} to={"/job_posting/"+jobPosting.id+"/edit"}>Edit</Button>
            <Button onClick={() => setDeleteModalOpen(true)}>Delete</Button>
        </span>
    }

    let jobDescriptionItem = null;
    if(jobPosting.job_description !== null){
        jobDescriptionItem = <Item>
            <Item.Content>
                <Item.Header>Job Description</Item.Header>
                <Item.Description>{jobPosting.description}</Item.Description>
            </Item.Content>
        </Item>
    }

    let jobBenefitsItem = null;
    if(jobPosting.benefits !== null){
                let labels = []
        let labelTexts = ["4 day work week", "RRSP Matching"]
        labelTexts.forEach(text => {
            labels.push(<Label tag color="blue">{text}</Label>)
        })
        let labelsExtra = null;
        if(labels.length > 0){
            labelsExtra = <Item.Extra>
                {labels}
            </Item.Extra>
        }

        jobBenefitsItem = <Item>
            <Item.Content>
                <Item.Header>Benefits</Item.Header>
                {labelsExtra}
                <Item.Description>{jobPosting.benefits}</Item.Description>
            </Item.Content>
        </Item>
    }

    let jobRequirementsItem = null;
    if(jobPosting.requirements !== null){
        jobRequirementsItem = <Item>
            <Item.Content>
                <Item.Header>Requirements</Item.Header>
                <Item.Description>{jobPosting.requirements}</Item.Description>
            </Item.Content>
        </Item>
    }

    let ApplyUntil = null;
    if(jobPosting.apply_until !== null && jobPosting.apply_until !== undefined){
        ApplyUntil = <Item.Extra>
            Open to applications until {jobPosting.apply_until}
        </Item.Extra>
    }

    return <>
        <MainMenu highlight={'Job Postings'}/>
        <Container>
            <Item.Group>
                <Item>
                    <Item.Image src={jobPosting.company.logo_url} size='tiny' />
                    <Item.Content>
                        <Item.Header>
                            {jobPosting.job_title} {adminMenu}
                        </Item.Header>
                        <Item.Extra as={Link} to={"/company/"+jobPosting.company.id}>
                            {jobPosting.company.name}
                        </Item.Extra>
                        <Item.Meta>
                            {jobPosting.min_salary}-{jobPosting.max_salary} {jobPosting.salary_currency}
                        </Item.Meta>
                    </Item.Content>
                </Item>
                {jobDescriptionItem}
                {jobRequirementsItem}
                {jobBenefitsItem}
                <Item>
                    <Item.Content>
                        <Item.Header>Applying</Item.Header>
                        {ApplyUntil}
                        <Item.Description>
                            <Button as={Link} to={jobPosting.application_url}>Apply</Button>
                        </Item.Description>
                    </Item.Content>
                </Item>
            </Item.Group>
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