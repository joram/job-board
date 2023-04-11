import {AuthenticationRequiredApi, Configuration, PublicApi} from "job-board-sdk";
import {serverUrl} from "./utils";

let config = new Configuration({
    basePath: serverUrl("")
})
let api = new PublicApi(config)
let privateApi = new AuthenticationRequiredApi(config)
let user = JSON.parse(sessionStorage.getItem("user"))

export function get_access_token() {
    return user.access_token
}

export function get_user_id() {
    return user.id
}


export async function get_all_companies() {
    return api.getCompaniesCompaniesGet().then((res) => {
        return res.data
    })
}


export async function get_my_companies() {
    return privateApi.getMyCompaniesUserUserIdCompaniesGet(user.id, user.access_token).then((res) => {
        return res.data
    })
}

export async function create_company(company) {
    return privateApi.postCompanyCompanyPost(company, user.access_token).then((res) => {
        return res.data
    })
}

export async function update_company(company) {
    return privateApi.putCompanyCompanyCompanyIdPut(company.id, company, user.access_token).then((res) => {
        console.log(res)
        return res
    })
}

export async function delete_company(company_id) {
    return privateApi.deleteCompanyCompanyCompanyIdDelete(company_id, user.access_token).then((res) => {
        return res
    })
}

export function create_job_posting(job_posting){
    return privateApi.post(job_posting, user.access_token).then((res) => {
        return res.data
    })
}


export async function get_all_job_postings() {
    return api.getPostingsPostingsGet().then((res) => {
        return res.data
    })
}

export async function get_company_by_id(id) {
    return api.getCompanyCompanyCompanyIdGet(id).then((res) => {
        return res.data
    })
}
