export function serverUrl(path) {
  if(window.location.hostname === 'localhost')
    return 'http://localhost:5000'+path

  return 'https://d9fr3dwx8e.execute-api.ca-central-1.amazonaws.com/prod'+path
}

export function clientUrl(path) {

    // https://d3hyaukyxs28vm.cloudfront.net/
    if(window.location.href.search("/") === 3){
        path = path.substring(1, path.length)
        let fullUrl = window.location.href+path
        return fullUrl
    }

    // https://d3hyaukyxs28vm.cloudfront.net/companies
    let rootUrl = window.location.href.replace(window.location.pathname, '')
    let fullUrl = rootUrl+path
    return fullUrl
}

export function getLocalUser(){
    let user_str = sessionStorage.getItem("user")
    if (user_str===undefined || user_str==="undefined") {
        return null
    }
    let user = JSON.parse(user_str)
    return user
}