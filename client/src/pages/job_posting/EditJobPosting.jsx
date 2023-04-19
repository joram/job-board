import React, {useEffect, useState} from 'react'
import {Button, Container, Form, Table} from "semantic-ui-react";
import MainMenu from "../../components/MainMenu";
import {get_job_posting, get_my_companies, get_user_id, update_job_posting} from "../../api";
import {useParams} from 'react-router-dom';

export default function EditJobPosting(){
    let [name, setName] = useState("")
    let [description, setDescription] = useState("")
    let [requirements, setRequirements] = useState("")
    let [benefits, setBenefits] = useState("")
    let [companyId, setCompanyId] = useState(null)
    let [applicationUrl, setApplicationUrl] = useState("")
    let [minimumSalary, setMinimumSalary] = useState(0)
    let [maximumSalary, setMaximumSalary] = useState(0)
    let [salaryCurrency, setSalaryCurrency] = useState("")
    let [companyOptions, setCompanyOptions] = useState([])
    let { job_posting_id } = useParams();

    function submit(){
        update_job_posting({
            id: job_posting_id,
            user_id: get_user_id(),
            job_title: name,
            description: description,
            requirements: requirements,
            benefits: benefits,
            company_id: companyId,
            application_url: applicationUrl,
            min_salary: minimumSalary,
            max_salary: maximumSalary,
            salary_currency: salaryCurrency
        }).then(r => {
            console.log(r)
        })
    }

    useEffect(() => {
        get_job_posting(job_posting_id).then(job_posting => {
            console.log(job_posting)
            setMinimumSalary(job_posting.min_salary)
            setMaximumSalary(job_posting.max_salary)
            setSalaryCurrency(job_posting.salary_currency)
            setBenefits(job_posting.benefits)
            setRequirements(job_posting.requirements)
            setName(job_posting.job_title)
            setDescription(job_posting.description)
            setApplicationUrl(job_posting.application_url)
            setCompanyId(job_posting.company.id)
        })
        get_my_companies().then(companies => {
            let options = companies.map(company => {
                return {
                    key: company.id,
                    text: company.name,
                    value: company.id
                }
            })
            options.push({
                key: "nan",
                text: "None",
                value: "nan"
            })
            setCompanyOptions(options)
        })
    }, [job_posting_id])

    return <>
        <MainMenu />
        <Container>
        <h1>Create Job Posting</h1>
        <Form onSubmit={() => submit()}>
            <Form.Input label="job title" input="text" onChange={(e) => setName(e.target.value)} value={name}/>
            <Form.TextArea label="description" input="textbox" onChange={e => setDescription(e.target.value)} value={description}/>
            <Form.TextArea label="requirements" input="textbox" onChange={e => setRequirements(e.target.value)} value={requirements}/>
            <Form.TextArea label="benefits" input="textbox" onChange={e => setBenefits(e.target.value)} value={benefits}/>
            <Form.Input label="application url" input="text" onChange={(e) => setApplicationUrl(e.target.value)} value={applicationUrl}/>
            <Form.Select label="company" placeholder="Optionally Select Company" options={companyOptions} onChange={(e, {value}) => setCompanyId(value)} value={companyId}/>
            <Table basic='very'>
                <Table.Row>
                    <Table.Cell>
                        <Form.Input label="minimum salary" input="number" onChange={(e) => setMinimumSalary(e.target.value)} value={minimumSalary}/>
                    </Table.Cell>
                    <Table.Cell>
                        <Form.Input label="maximum salary" input="number" onChange={(e) => setMaximumSalary(e.target.value)} value={maximumSalary}/>
                    </Table.Cell>
                    <Table.Cell>
                        <Form.Input label="salary currency" input="text" onChange={(e) => setSalaryCurrency(e.target.value)} value={salaryCurrency}/>
                    </Table.Cell>
                </Table.Row>
            </Table>
            <Button type='submit'>Save</Button>
          </Form>
    </Container>
        </>
}