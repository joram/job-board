import React, {useState} from 'react'
import {Button, Container, Form} from "semantic-ui-react";
import MainMenu from "../components/MainMenu";
import {create_company, get_user_id} from "../api";
import {useNavigate} from "react-router";

export default function CreateCompany(){
    let [value, setValue] = useState("<=10")
    let [name, setName] = useState("")
    let [description, setDescription] = useState("")
    let [website, setWebsite] = useState("")
    let [logo, setLogo] = useState("")
    let [address, setAddress] = useState("")
    let navigate = useNavigate();
    function submit(){
        create_company({
            user_id: get_user_id(),
            name: name,
            description: description,
            website_url: website,
            logo_url: logo,
            size: value,
            address: address,
        }).then(() => {
            console.log("Company created")
            navigate("/my/companies/")
        })
    }
    return <>
        <MainMenu />
        <Container>
        <h1>Create New Company</h1>
        <Form onSubmit={() => submit()}>
            <Form.Input label="name" input="text" onChange={(e) => setName(e.target.value)}/>
            <Form.TextArea label="description" input="textbox" onChange={e => setDescription(e.target.value)}/>
            <Form.Input label="website" input="text" placeholder="https://domain.com" onChange={e => setWebsite(e.target.value)}/>
            <Form.Input label="logo" input="text" placeholder="https://domain.com/logo.png" onChange={e => setLogo(e.target.value)}/>
            <Form.Group inline>
              <label>Size</label>
              <Form.Radio
                label='<=10'
                value='<=10'
                checked={value === '<=10'}
                onChange={() => setValue("<=10")}
              />
              <Form.Radio
                label='11-20'
                value='11-20'
                checked={value === '11-20'}
                onChange={() => setValue("11-20")}
              />
              <Form.Radio
                label='21-50'
                value='21-50'
                checked={value === '21-50'}
                onChange={() => setValue("21-50")}
              />
              <Form.Radio
                label='51-100'
                value='51-100'
                checked={value === '51-100'}
                onChange={() => setValue("51-100")}
              />
              <Form.Radio
                label='101-500'
                value='101-500'
                checked={value === '101-500'}
                onChange={() => setValue("101-500")}
              />
              <Form.Radio
                label='>=500'
                value='>=500'
                checked={value === '>=500'}
                onChange={() => setValue(">=500")}
              />
            </Form.Group>
            <Form.Input label="address" input="text" placeholder={"123 Fort st, H0H0H0 Victoria BC Canada"} onChange={e => setAddress(e.target.value)}/>
            <Button type='submit'>Submit</Button>
          </Form>
    </Container>
        </>
}