import {Configuration, PublicApi} from "job-board-sdk";
import {serverUrl} from "./utils";

let config = new Configuration({
    basePath: serverUrl("")
})
let api = new PublicApi(config)


export async function get_all_companies() {
    return api.getCompaniesCompaniesGet().then((res) => {
        return res.data
    })
}


export async function get_all_job_postings() {
    return api.getPostingsPostingsGet().then((res) => {
        return res.data
    })
}
