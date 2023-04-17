export function serverUrl(path) {
  if(window.location.hostname === 'localhost')
    return 'http://localhost:5000'+path

  return 'https://d9fr3dwx8e.execute-api.ca-central-1.amazonaws.com/prod'+path
}
function getPosition(string, subString, index) {
    return string.split(subString, index).join(subString).length;
}

export function clientUrl(path) {
    let url = window.location.href
    url = url.substring(0, getPosition(url, '/', 3))
    url = url+path
    return url
}

export function getLocalUser(){
    let user_str = sessionStorage.getItem("user")
    if (user_str===undefined || user_str==="undefined") {
        return null
    }
    let user = JSON.parse(user_str)
    return user
}

export function truncate(str, n){
  return (str.length > n) ? str.slice(0, n-1) + '...' : str;
}