import {AuthenticationRequiredApi, Configuration, PublicApi} from "job-board-sdk";
import {serverUrl} from "./utils";

let config = new Configuration({
    basePath: serverUrl("")
})
let api = new PublicApi(config)
let privateApi = new AuthenticationRequiredApi(config)

function get_user() {
    let user = JSON.parse(sessionStorage.getItem("user"))
    return user
}

export function get_accessToken() {
    return get_user().accessToken
}

export function get_user_id() {
    let user = get_user()
    return user !== null ? user.id : 0
}

let options = {
    withCredentials: false,
}


export async function get_all_companies() {
    return api.getCompaniesCompaniesGet(options).then((res) => {
        return res.data
    })
}


export async function get_my_companies() {
    let user = get_user()
    console.log(user)
    return privateApi.getMyCompaniesUserUserIdCompaniesGet(user.id, user.accessToken).then((res) => {
        return res.data
    })
}

export async function get_my_job_postings() {
    let user = get_user()
    return privateApi.getMyPostingsUserUserIdPostingsGet(user.id, user.accessToken).then((res) => {
        return res.data
    })
}

export async function create_company(company) {
    let user = get_user()
    return privateApi.postCompanyCompanyPost(company, user.accessToken).then((res) => {
        return res.data
    })
}

export async function update_company(company) {
    let user = get_user()
    return privateApi.putCompanyCompanyCompanyIdPut(company.id, company, user.accessToken).then((res) => {
        console.log(res)
        return res
    })
}

export async function delete_company(company_id) {
    let user = get_user()
    return privateApi.deleteCompanyCompanyCompanyIdDelete(company_id, user.accessToken).then((res) => {
        return res
    })
}

export function create_job_posting(job_posting){
    let user = get_user()
    return privateApi.post(job_posting, user.accessToken).then((res) => {
        return res.data
    })
}


export async function get_all_job_postings() {
    return api.getPostingsPostingsGet(options).then((res) => {
        return res.data
    })
}

export async function get_company_by_id(id) {
    return api.getCompanyCompanyCompanyIdGet(id, options).then((res) => {
        return res.data
    })
}
