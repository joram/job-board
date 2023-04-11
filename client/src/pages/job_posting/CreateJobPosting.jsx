import React, {useEffect, useState} from 'react'
import {Button, Container, Form, Table} from "semantic-ui-react";
import MainMenu from "../../components/MainMenu";
import {create_job_posting, get_my_companies, get_user_id} from "../../api";

export default function CreateJobPosting(){
    let [name, setName] = useState("")
    let [description, setDescription] = useState("")
    let [benefits, setBenefits] = useState("")
    let [companyId, setCompanyId] = useState(null)
    let [applicationUrl, setApplicationUrl] = useState("")
    let [minimumSalary, setMinimumSalary] = useState(0)
    let [maximumSalary, setMaximumSalary] = useState(0)
    let [salaryCurrency, setSalaryCurrency] = useState("")
    let [companyOptions, setCompanyOptions] = useState([])

    function submit(){
        create_job_posting({
            user_id: get_user_id(),
            name: name,
            description: description,
        }).then(r => {
            console.log(r)
        })
    }

    useEffect(() => {
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
    }, [])

    return <>
        <MainMenu />
        <Container>
        <h1>Create Job Posting</h1>
        <Form onSubmit={() => submit()}>
            <Form.Input label="job title" input="text" onChange={(e) => setName(e.target.value)} value={name}/>
            <Form.TextArea label="description" input="textbox" onChange={e => setDescription(e.target.value)} value={description}/>
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
            <Button type='submit'>Submit</Button>
          </Form>
    </Container>
        </>
}